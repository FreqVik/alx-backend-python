from rest_framework import generics, viewsets
from .models import User, Message, Conversation
from .serializers import UserSerializer, MessageSerializer, ConversationSerializer


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    lookup_field = 'id'
    http_method_names = ['get', 'post', 'put', 'delete']


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    lookup_field = 'id'
    http_method_names = ['get', 'post', 'put', 'delete']


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'
    http_method_names = ['get', 'post', 'put', 'delete']