from django.urls import path, include
from django.views.generic import TemplateView

from .views import (
    FileListView,
    FileDetailView,
    FileAnonUploadView,
    FileAuthUploadView,
    fileDownloadView,
)


urlpatterns = [
    path('upload/', TemplateView.as_view(template_name='file_upload.html'), name='file_upload'),
    path('<slug:slug>/download/', fileDownloadView, name='file_download'),
    path('upload-anon/', FileAnonUploadView.as_view(), name='file_anon_upload'),
    path('upload-auth/', FileAuthUploadView.as_view(), name='file_auth_upload'),
    path('<slug:slug>/', FileDetailView.as_view(), name='file_detail'),
    path('', FileListView.as_view(), name='file_list'),
]
