import requests
from prometheus_client.parser import text_string_to_metric_families

MINIO_URL = "http://127.0.0.1:9000/minio/v2/metrics/cluster"
MINIO_USER = "admin"
MINIO_PASSWORD = "strongpassword"

def fetch_minio_metrics():
    """
    Fetches MinIO cluster metrics dynamically and parses them into a structured dictionary.
    """
    try:
        print(f"Fetching MinIO metrics from {MINIO_URL}...")

        # Attempt unauthenticated request first
        response = requests.get(MINIO_URL)

        # Retry with authentication if needed
        if response.status_code in [400, 401]:
            print(" Unauthorized or Bad Request! Retrying with authentication...")
            response = requests.get(MINIO_URL, auth=(MINIO_USER, MINIO_PASSWORD))

        response.raise_for_status()

        print(f"Response Code: {response.status_code}")
        print(f"Response Body: {response.text[:500]}")  # Print first 500 chars

        metrics = {}
        for family in text_string_to_metric_families(response.text):
            for sample in family.samples:
                metrics[sample.name] = sample.value

        print(f"Extracted Metrics: {metrics}")

        # Extracting cluster-level data
        cluster_metrics = {
            "nodes_online": int(metrics.get("minio_cluster_nodes_online_total", 0)),
            "nodes_offline": int(metrics.get("minio_cluster_nodes_offline_total", 0)),
            "total_storage": metrics.get("minio_cluster_capacity_usable_total_bytes", 0),
            "used_storage": metrics.get("minio_cluster_usage_total_bytes", 0),
            "free_storage": float(metrics.get("minio_cluster_capacity_usable_total_bytes", 0)) - float(metrics.get("minio_cluster_usage_total_bytes", 0)),
            "node_health": "✅ Healthy" if metrics.get("minio_cluster_health_status", 0) == 1 else "❌ Unhealthy",
            "buckets_total": int(metrics.get("minio_cluster_bucket_total", 0)),
            "objects_total": int(metrics.get("minio_cluster_usage_object_total", 0)),
            "node_details": []
        }

        # Extracting per-node statistics dynamically
        total_nodes = cluster_metrics["nodes_online"] + cluster_metrics["nodes_offline"]
        for node_id in range(1, total_nodes + 1):
            node_metrics = {
                "node_id": node_id,
                "cpu_usage": metrics.get(f"minio_node_process_cpu_total_seconds_total", "N/A"),
                "memory_usage": metrics.get(f"minio_node_process_resident_memory_bytes", "N/A"),
                "disk_read": metrics.get(f"minio_node_io_read_bytes_total", "N/A"),
                "disk_write": metrics.get(f"minio_node_io_write_bytes_total", "N/A"),
                "online": metrics.get("minio_cluster_nodes_online_total", 0) > 0
            }
            cluster_metrics["node_details"].append(node_metrics)

        return cluster_metrics

    except requests.exceptions.RequestException as e:
        print(f"Error fetching MinIO metrics: {e}")
        return None


# import requests
# from prometheus_client.parser import text_string_to_metric_families

# MINIO_URL = "http://127.0.0.1:9000/minio/v2/metrics/cluster"
# MINIO_USER = "admin"
# MINIO_PASSWORD = "strongpassword"

# def fetch_minio_metrics():
#     """
#     Fetches MinIO cluster metrics and parses them into a dictionary.
#     """
#     try:
#         print(f"Fetching MinIO metrics from {MINIO_URL}...")

#         # Try unauthenticated request first
#         response = requests.get(MINIO_URL)

#         # If it fails, retry with authentication
#         if response.status_code in [400, 401]:
#             print(" Unauthorized or Bad Request! Retrying with authentication...")
#             response = requests.get(MINIO_URL, auth=(MINIO_USER, MINIO_PASSWORD))

#         response.raise_for_status()

#         print(f"Response Code: {response.status_code}")
#         print(f" Response Body: {response.text[:500]}")  # Print first 500 chars

#         metrics = {}
#         for family in text_string_to_metric_families(response.text):
#             for sample in family.samples:
#                 metrics[sample.name] = sample.value

#         print(f" Extracted Metrics: {metrics}")
#         return metrics

#     except requests.exceptions.RequestException as e:
#         print(f" Error fetching MinIO metrics: {e}")
#         return None