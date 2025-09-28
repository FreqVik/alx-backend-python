from rest_framework import permissions
from .models import Conversation, Message, User

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to access it.
    Allows participants to send (POST), view (GET), update (PUT/PATCH), and delete (DELETE) messages.
    """
    def has_permission(self, request, view):
        # First check if user is authenticated
        if not request.user.is_authenticated:
            return False
        
        # For creating new conversations, always allow authenticated users
        if view.action == 'create':
            return True
            
        # For listing conversations, allow authenticated users (queryset will filter)
        if view.action == 'list':
            return True
            
        # For detail views, we need to check object-level permissions
        if view.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            # For detail views, we'll rely on has_object_permission
            return True
        
        # Default allow for authenticated users
        return True
    
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        
        # Check specific HTTP methods for messages and conversations
        if request.method in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']:
            # Handle both Conversation and Message objects
            if isinstance(obj, Conversation):
                return self.is_participant(request.user, obj)
            elif isinstance(obj, Message):
                # For messages, check if user is participant of the conversation
                return self.is_participant(request.user, obj.conversation)
        
        return False
    
    def is_participant(self, user, conversation):
        """
        Allow only participants in a conversation to send, view, update and delete messages
        """
        return conversation.participants.filter(pk=user.pk).exists()