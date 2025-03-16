import os
import aiofiles
from .minio_client import minio_client, BUCKET_NAME

CHUNK_SIZE = 5 * 1024 * 1024  # 5MB chunks

async def save_file_chunks(file, file_name):
    """Splits file into chunks and uploads to MinIO"""
    chunk_index = 0
    file_id = file_name  # Unique identifier for file reconstruction

    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)

    async with aiofiles.open(f"{upload_dir}/{file_name}", "wb") as temp_file:
        while chunk := await file.read(CHUNK_SIZE):
            await temp_file.write(chunk)

    async with aiofiles.open(f"{upload_dir}/{file_name}", "rb") as temp_file:
        while chunk := await temp_file.read(CHUNK_SIZE):
            chunk_name = f"{file_id}_chunk_{chunk_index}"
            minio_client.put_object(BUCKET_NAME, chunk_name, temp_file, len(chunk))
            chunk_index += 1

    return {"message": "File uploaded in chunks", "chunks": chunk_index}

async def retrieve_file(file_name):
    """Retrieves chunks from MinIO and reconstructs the file"""
    chunk_index = 0
    reconstructed_file_path = f"downloads/{file_name}"

    os.makedirs("downloads", exist_ok=True)

    async with aiofiles.open(reconstructed_file_path, "wb") as output_file:
        while True:
            chunk_name = f"{file_name}_chunk_{chunk_index}"
            try:
                chunk_data = minio_client.get_object(BUCKET_NAME, chunk_name)
                await output_file.write(chunk_data.read())
                chunk_index += 1
            except Exception:
                break  # No more chunks

    return {"message": "File reconstructed", "path": reconstructed_file_path}