from rest_framework import permissions
from .models import Conversation, Message, User

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to access it.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        # For conversation views
        if hasattr(view, 'get_object'):
            try:
                obj = view.get_object()
                if isinstance(obj, Conversation):
                    return self.is_participant(request.user, obj)
                elif isinstance(obj, Message):
                    return self.is_participant(request.user, obj.conversation)
            except:
                pass

        return True
    
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        
        # Handle both Conversation and Message objects
        if isinstance(obj, Conversation):
            return self.is_participant(request.user, obj)
        elif isinstance(obj, Message):
            return self.is_participant(request.user, obj.conversation)
        
        return False
    
    def is_participant(self, user, conversation):
        """
        Allow only participants in a conversation to send, view, update and delete messages
        """
        return conversation.participants.filter(id=user.id).exists()