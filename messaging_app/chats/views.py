from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer, UserSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Add the requesting user as a participant
        conversation = serializer.save()
        conversation.participants.add(self.request.user)
        conversation.save()

    def get_queryset(self):
        # Only show conversations the user participates in
        return Conversation.objects.filter(participants=self.request.user)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        conversation = serializer.validated_data['conversation']
        if self.request.user not in conversation.participants.all():
            raise ValidationError("You are not a participant in this conversation.")
        serializer.save(sender=self.request.user)

    def get_queryset(self):
        return Message.objects.filter(conversation__participants=self.request.user)

# Create your views here.

