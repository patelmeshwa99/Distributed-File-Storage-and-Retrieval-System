from io import BytesIO
import io
from django.http import JsonResponse
from minio import Minio
from django.conf import settings
from ..models import File
import asyncio
import sys
import os


sys.path.append(os.path.abspath(".."))
from kademlia_server import node

minio_client = Minio(
    settings.MINIO_ENDPOINT,
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=False
)

def upload_file_chunk(file_path, chunk_data, chunk_name):
    # Upload the chunk to MinIO
    minio_client.put_object(
        bucket_name=settings.MINIO_BUCKET,
        object_name=chunk_name,
        data=io.BytesIO(chunk_data),
        length=len(chunk_data)
    )

def bucket_exists_check(bucket_name):
    return minio_client.bucket_exists(bucket_name)

def make_bucket(bucket_name):
    minio_client.make_bucket(bucket_name)

def get_chunk_from_minio(chunk_name):
    """Retrieves a file chunk from MinIO."""
    try:
        response = minio_client.get_object(settings.MINIO_BUCKET, chunk_name)
        
        # Read data into memory
        chunk_data = BytesIO(response.read())

        return chunk_data.getvalue()  # Return the chunk as bytes

    except Exception as e:
        print(f"Error retrieving chunk {chunk_name}: {e}")
        return None  # Return None if chunk retrieval fails

def handle_file_chunking(uploaded_file, chunk_size=10 * 1024 * 1024):
    file_data = uploaded_file.read()
    total_size = len(file_data)
    file_name = uploaded_file.name
    chunk_count = total_size // chunk_size + (1 if total_size % chunk_size > 0 else 0)
    chunk_names = []

    for i in range(chunk_count):
        chunk = file_data[i*chunk_size:(i+1)*chunk_size]
        chunk_name = f"{file_name}_chunk_{i}"
        upload_file_chunk(file_name, chunk, chunk_name)
        chunk_names.append(chunk_name)

    # Save file metadata to database
    # await sync_to_async(FileMetadata.objects.create)(
    #         file_hash=file_hash, chunk_location=chunk_location
    #     )
    # file_instance = File.objects.create(
    #     file_name=file_name,
    #     file_size=total_size,
    #     chunk_count=chunk_count
    # )

    return chunk_names

async def process_file(uploaded_file):
    # Handle chunking and upload to MinIO
    chunk_names = handle_file_chunking(uploaded_file, chunk_size=10*1024*1024)

    # Store metadata in Kademlia
    # dht_peer = DHTPeer(port=8468)
    await node.store_metadata(uploaded_file.name, str(chunk_names).encode("utf-8"))
    # await dht_peer.store_metadata(uploaded_file.name, str(chunk_names).encode("utf-8"))

    return JsonResponse({"message": "File uploaded successfully!"})