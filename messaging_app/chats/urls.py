from django.urls import path, include
from rest_framework.routers import DefaultRouter as routers
from .views import ConversationViewSet, MessageViewSet

router = routers()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('', include(router.urls)),
]
