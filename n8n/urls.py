from django.urls import path
from . import views

urlpatterns = [
    # 工作流管理API
    path('api/n8n/workflows/', views.workflow_list, name='workflow_list'),
    path('api/n8n/workflows/<int:pk>/', views.workflow_detail, name='workflow_detail'),
    path('api/n8n/workflows/create/', views.workflow_create, name='workflow_create'),
    path('api/n8n/workflows/<int:pk>/update/', views.workflow_update, name='workflow_update'),
    path('api/n8n/workflows/<int:pk>/delete/', views.workflow_delete, name='workflow_delete'),
    # 工作流执行API
    path('api/n8n/workflows/<int:pk>/execute/', views.workflow_execute, name='workflow_execute'),
    # 工作流执行历史API
    path('api/n8n/executions/', views.execution_list, name='execution_list'),
    path('api/n8n/executions/<int:pk>/', views.execution_detail, name='execution_detail'),
]
