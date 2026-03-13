from django.urls import path
from .views import KnowledgeInfoListView, KnowledgeInfoCreateView, KnowledgeInfoDetailView, KnowledgeInfoUpdateView, KnowledgeInfoDeleteView, KnowledgeAttachListView, KnowledgeAttachUploadView, KnowledgeAttachDeleteView

urlpatterns = [
    path('info/', KnowledgeInfoListView.as_view(), name='knowledge_list'),
    path('info/create/', KnowledgeInfoCreateView.as_view(), name='knowledge_create'),
    path('info/<int:knowledge_id>/', KnowledgeInfoDetailView.as_view(), name='knowledge_detail'),
    path('info/<int:knowledge_id>/update/', KnowledgeInfoUpdateView.as_view(), name='knowledge_update'),
    path('info/<int:knowledge_id>/delete/', KnowledgeInfoDeleteView.as_view(), name='knowledge_delete'),
    path('info/<int:knowledge_id>/attachments/', KnowledgeAttachListView.as_view(), name='knowledge_attachments'),
    path('info/<int:knowledge_id>/attachments/upload/', KnowledgeAttachUploadView.as_view(), name='knowledge_attach_upload'),
    path('attachments/<int:attach_id>/delete/', KnowledgeAttachDeleteView.as_view(), name='knowledge_attach_delete'),
]
