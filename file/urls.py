from django.urls import path
from .views import FileUploadView, FileListView, FileDeleteView

urlpatterns = [
    path('upload/', FileUploadView.as_view(), name='file_upload'),
    path('list/', FileListView.as_view(), name='file_list'),
    path('delete/<int:file_id>/', FileDeleteView.as_view(), name='file_delete'),
]
