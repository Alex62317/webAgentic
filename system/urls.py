from django.urls import path
from .views import SysConfigListView, SysConfigCreateView, SysConfigDetailView, SysConfigUpdateView, SysConfigDeleteView

urlpatterns = [
    path('config/', SysConfigListView.as_view(), name='sys_config_list'),
    path('config/create/', SysConfigCreateView.as_view(), name='sys_config_create'),
    path('config/<int:config_id>/', SysConfigDetailView.as_view(), name='sys_config_detail'),
    path('config/<int:config_id>/update/', SysConfigUpdateView.as_view(), name='sys_config_update'),
    path('config/<int:config_id>/delete/', SysConfigDeleteView.as_view(), name='sys_config_delete'),
]
