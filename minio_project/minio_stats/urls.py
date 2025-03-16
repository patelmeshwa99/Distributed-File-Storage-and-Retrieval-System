from django.urls import path
from .views import minio_status

urlpatterns = [
    path('', minio_status, name='minio_status'),
]
