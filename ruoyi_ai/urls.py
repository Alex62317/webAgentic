"""
URL configuration for ruoyi_ai project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from .views import home, set_language, langchain_chat, crewai_task

# API文档配置
schema_view = get_schema_view(
   openapi.Info(
      title="AI API",
      default_version='v1',
      description="企业级AI助手平台API文档",
      terms_of_service="https://www.example.com/terms/",
      contact=openapi.Contact(email="admin@example.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', home, name='index'),
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls')),
    path('chat/', include('chat.urls')),
    path('knowledge/', include('knowledge.urls')),
    path('system/', include('system.urls')),
    path('file/', include('file.urls')),
    # AI功能路由
    path('api/ai/langchain/', langchain_chat, name='langchain_chat'),
    path('api/ai/crewai/', crewai_task, name='crewai_task'),
    # n8n相关路由
    path('', include('n8n.urls')),
    # 语言切换路由
    path('set-language/', set_language, name='set_language'),
    # API文档路由
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# Add media files URL
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
