from minio import Minio
from minio.error import S3Error

# MinIO client initialization
client = Minio(
    "localhost:9000",
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False
)

bucket_name = "bucket-01"

try:
    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)
        print(f"Created bucket {bucket_name}")
except S3Error as e:
    print(f"Error: {e}")