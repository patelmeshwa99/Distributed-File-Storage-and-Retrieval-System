from django.db import models

# Create your models here.
class FileMetadata(models.Model):
    file_name = models.CharField(max_length=255)
    file_size = models.BigIntegerField()  # Stores file size in bytes
    storage_location = models.TextField()  # MinIO path or local path
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Auto timestamp

    def __str__(self):
        return self.file_name