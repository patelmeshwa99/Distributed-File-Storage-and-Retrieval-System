from minio import Minio
import os

# MinIO connection details
MINIO_ENDPOINT = "localhost:9001"  # Corrected API port
ACCESS_KEY = os.getenv("MINIO_ROOT_USER", "admin")
SECRET_KEY = os.getenv("MINIO_ROOT_PASSWORD", "password")  
BUCKET_NAME = "file-chunks"

# Initialize MinIO client
minio_client = Minio(
    MINIO_ENDPOINT,
    access_key=ACCESS_KEY,
    secret_key=SECRET_KEY,
    secure=False  # Disable SSL for local setup
)

# Ensure bucket exists
def ensure_bucket():
    if not minio_client.bucket_exists(BUCKET_NAME):
        minio_client.make_bucket(BUCKET_NAME)

ensure_bucket()