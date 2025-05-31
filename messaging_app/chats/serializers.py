from rest_framework import serializers
from .models import Conversation, Message, User


class UserSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class ConversationSerializer(serializers.ModelSerializer):
    chat_id = serializers.UUIDField(read_only=True)
    participants = UserSerializer(many=True, read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Conversation
        fields = ['chat_id', 'participants', 'created_at']


class MessageSerializer(serializers.ModelSerializer):
    message_id = serializers.UUIDField(read_only=True)
    conversation = serializers.PrimaryKeyRelatedField(queryset=Conversation.objects.all())
    sender = UserSerializer(read_only=True)
    content = serializers.CharField(required=True, allow_blank=False)
    timestamp = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Message
        fields = ['message_id', 'conversation', 'sender', 'content', 'timestamp']
