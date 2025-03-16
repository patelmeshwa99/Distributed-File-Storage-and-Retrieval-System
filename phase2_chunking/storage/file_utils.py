import os
from .minio_client import client

CHUNK_SIZE = 5 * 1024 * 1024  # 5MB chunks
BUCKET_NAME = "bucket-01"

def chunk_and_upload(file):
    """Splits a file into chunks and uploads each to MinIO."""
    index = 0
    uploaded_chunks = []

    while True:
        chunk = file.read(CHUNK_SIZE)
        if not chunk:
            break

        chunk_name = f"{file.name}.part{index}"

        # Save chunk temporarily
        temp_path = f"/tmp/{chunk_name}"
        with open(temp_path, "wb") as chunk_file:
            chunk_file.write(chunk)

        # Upload chunk to MinIO
        client.fput_object(BUCKET_NAME, chunk_name, temp_path)

        # Cleanup local temp file
        os.remove(temp_path)

        uploaded_chunks.append(chunk_name)
        index += 1

    return uploaded_chunks  # Return the list of chunk names
