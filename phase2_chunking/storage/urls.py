from django.urls import path
from .views import upload_large_file  # Import the view

urlpatterns = [
    path('upload-chunks/', upload_large_file, name='upload-large-file'),
]