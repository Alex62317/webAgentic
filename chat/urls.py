from django.urls import path
from .views import ChatModelListView, ChatSessionListView, ChatSessionCreateView, ChatSessionDeleteView, ChatMessageListView, ChatSendView, chat_index

urlpatterns = [
    path('', chat_index, name='chat_index'),
    path('models/', ChatModelListView.as_view(), name='chat_models'),
    path('sessions/', ChatSessionListView.as_view(), name='chat_sessions'),
    path('sessions/create/', ChatSessionCreateView.as_view(), name='chat_session_create'),
    path('sessions/<int:session_id>/delete/', ChatSessionDeleteView.as_view(), name='chat_session_delete'),
    path('sessions/<int:session_id>/messages/', ChatMessageListView.as_view(), name='chat_messages'),
    path('send/', ChatSendView.as_view(), name='chat_send'),
]
