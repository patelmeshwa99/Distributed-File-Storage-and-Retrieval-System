from django.http import HttpResponse, JsonResponse
from minio import Minio
from minio.error import S3Error
from django.conf import settings
import sys, os
import requests
from .utils.utils import bucket_exists_check, get_chunk_from_minio, make_bucket, process_file

sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from kademlia_server import node

def sign_up(request):
    name = "meshwa"
    try:
        # Test connection by checking the MinIO bucket
        if bucket_exists_check(name):
            return JsonResponse(
                {"error": "Internal Server Error", "code": "USER_ALREADY_EXIST"}, 
                status=500
            )
        else:
            print("Bucket does not exist")
            make_bucket(name)
        
        return HttpResponse("Connection to MinIO successful!")
    
    except S3Error as e:
        return HttpResponse(f"Error connecting to MinIO: {str(e)}", status=500)

async def upload_file(request):
    name = "meshwa"
    
    # Create minIO client
    try:
        # Test connection by checking the MinIO bucket
        if bucket_exists_check(name):
            # process_file(request.FILES['file'])
            await process_file(open("/Users/meshwa/Desktop/lab6-2.png", 'rb'))
        return HttpResponse("Connection to MinIO successful!")
    
    except S3Error as e:
        return HttpResponse(f"Error connecting to MinIO: {str(e)}", status=500)

def request_chunk_from_peer(chunk_name):
    """Request a file chunk from a peer via WebRTC signaling."""
    signaling_server = "http://your-signaling-server.com/get_chunk"
    
    response = requests.post(signaling_server, json={"chunk_name": chunk_name})

    if response.status_code == 200:
        return response.content  # Return chunk data if found
    else:
        return None  # Peer not available, fallback needed

async def download_file(request):
        file_name='lab6-1.png'
        # Fetch chunk locations from Kademlia
        chunk_locations = await node.get_metadata(file_name)

        if not chunk_locations:
            return JsonResponse({"error": "File not found"}, status=404)
        
        file_chunks = {}
        # Fetch data from peer first
        for chunk_name in chunk_locations:
            peer_chunk = request_chunk_from_peer(chunk_name)
            if peer_chunk:
                    file_chunks[chunk_name] = peer_chunk
            else:
                # 2️⃣ If no peer has it, fetch from MinIO
                    file_chunks[chunk_name] = get_chunk_from_minio(chunk_name)

        return JsonResponse({"file_name": file_name, "chunk_locations": chunk_locations})
