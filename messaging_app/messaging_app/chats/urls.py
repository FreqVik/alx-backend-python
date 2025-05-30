from .views import MessageViewSet, ConversationViewSet, UserViewSet
from django.urls import path
from rest_framework.routers import DefaultRouter
from django.urls import include


router = DefaultRouter()
router.register(r'conversations', ConversationViewSet)
router.register(r'messages', MessageViewSet)

# The urlpatterns list routes URLs to views. For more information please see:
urlpatterns = [
    path('/api', include(router.urls)),
]