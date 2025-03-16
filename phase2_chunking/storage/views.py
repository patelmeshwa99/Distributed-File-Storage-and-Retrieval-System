from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .file_utils import chunk_and_upload

# Create your views here.
@csrf_exempt
def upload_large_file(request):
    """API to upload a large file in chunks to MinIO."""
    if request.method == "POST":
        file = request.FILES.get("file")
        if not file:
            return JsonResponse({"error": "No file provided"}, status=400)

        chunk_list = chunk_and_upload(file)  # Call the chunking and upload function

        return JsonResponse({
            "message": "File uploaded in chunks successfully!",
            "chunks": chunk_list
        })

    return JsonResponse({"error": "Only POST method allowed"}, status=405)
