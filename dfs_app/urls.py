from django.urls import path, re_path
from . import views
app_name = 'dfs_app'
urlpatterns = [
    path(r'', views.sign_up, name='sign_up'),
    path(r'upload_file', views.upload_file, name='upload_file'),
    path(r'download_file', views.download_file, name='download_file')
]