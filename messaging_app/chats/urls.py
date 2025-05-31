from django.urls import path, include
from rest_framework.routers import DefaultRouter as routers
from .views import ConversationViewSet, MessageViewSet

routers.DefaultRouter()
routers.register(r'conversations', ConversationViewSet, basename='conversation')
routers.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('', include(routers.urls)),
]
