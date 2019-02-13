from django.urls import path, include
from django.views.generic import TemplateView

from .views import (
    FileListView,
    FileDetailView,
    FileAnonCreateView,
    FileAuthCreateView,
    FileAnonUploadView,
    FileAuthUploadView,
    fileDownloadView,
)


urlpatterns = [
    path('create/', TemplateView.as_view(template_name='file_create_general.html'), name='file_create'),
    path('create/create-anon/', FileAnonCreateView.as_view(), name='file_anon_create'),
    path('create/create-auth/', FileAuthCreateView.as_view(), name='file_auth_create'),
    path('upload/', TemplateView.as_view(template_name='file_upload_general.html'), name='file_upload'),
    path('<slug:slug>/download/', fileDownloadView, name='file_download'),
    path('upload/upload-anon/', FileAnonUploadView.as_view(), name='file_anon_upload'),
    path('upload/upload-auth/', FileAuthUploadView.as_view(), name='file_auth_upload'),
    path('<slug:slug>/', FileDetailView.as_view(), name='file_detail'),
    path('', FileListView.as_view(), name='file_list'),
]
