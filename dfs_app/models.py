from django.db import models

class File(models.Model):
    file_name = models.CharField(max_length=255)
    file_size = models.BigIntegerField()
    chunk_count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file_name
