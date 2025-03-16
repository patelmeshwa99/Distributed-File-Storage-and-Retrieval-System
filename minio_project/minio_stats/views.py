from django.shortcuts import render
from .metrics import fetch_minio_metrics

def minio_status(request):
    """
    Fetch MinIO cluster metrics and dynamically render them in a web page.
    """
    metrics = fetch_minio_metrics()
    
    if not metrics:
        return render(request, 'minio_stats/error.html', {"message": "Failed to fetch MinIO metrics."})

    context = {
        'node_health': metrics["node_health"],
        'nodes_online': metrics["nodes_online"],
        'nodes_offline': metrics["nodes_offline"],
        'total_storage': metrics["total_storage"],
        'used_storage': metrics["used_storage"],
        'free_storage': metrics["free_storage"],
        'buckets_total': metrics["buckets_total"],
        'objects_total': metrics["objects_total"],
        'node_details': metrics["node_details"]
    }

    return render(request, 'minio_stats/minio_status.html', context)


# from django.shortcuts import render
# from .metrics import fetch_minio_metrics

# def minio_status(request):
#     """
#     Fetch MinIO cluster metrics and render them in a web page.
#     """
#     metrics = fetch_minio_metrics()

#     if not metrics:
#         return render(request, 'minio_stats/error.html', {"message": "Failed to fetch MinIO metrics."})

#     context = {
#         'node_health': "Healthy" if metrics.get('minio_cluster_health_status') == 1.0 else "Unhealthy",
#         'nodes_online': metrics.get('minio_cluster_nodes_online_total', 'Unknown'),
#         'nodes_offline': metrics.get('minio_cluster_nodes_offline_total', 'Unknown'),
#         'total_storage': metrics.get('minio_cluster_capacity_usable_total_bytes', 'Unknown'),
#         'used_storage': metrics.get('minio_cluster_usage_total_bytes', 'Unknown'),
#         'free_storage': metrics.get('minio_cluster_capacity_usable_free_bytes', 'Unknown'),
#         'total_buckets': metrics.get('minio_cluster_bucket_total', 'Unknown'),
#         'total_objects': metrics.get('minio_cluster_usage_object_total', 'Unknown'),
#     }

#     return render(request, 'minio_stats/minio_status.html', context)
