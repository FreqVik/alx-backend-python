from rest_framework import serializers
from .models import Conversation, Message, User


class UserSerializer(serializers.ModelSerializer):
    user_id = serializers.UUIDField(read_only=True)
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user



class MessageSerializer(serializers.ModelSerializer):
    message_id = serializers.UUIDField(read_only=True)
    conversation = serializers.PrimaryKeyRelatedField(queryset=Conversation.objects.all())
    sender = UserSerializer(read_only=True)
    message_body = serializers.CharField(required=True, allow_blank=False)
    timestamp = serializers.DateTimeField(read_only=True)

    def validate_message_body(self, value):
        if not value.strip():
            raise serializers.ValidationError("Message content cannot be empty or whitespace.")
        return value

    class Meta:
        model = Message
        fields = ['message_id', 'conversation', 'sender', 'message_body', 'timestamp']




class ConversationSerializer(serializers.ModelSerializer):
    conversation_id = serializers.UUIDField(read_only=True)
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    participant_count = serializers.SerializerMethodField()

    def get_participant_count(self, obj):
        return obj.participants.count()

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages', 'created_at', 'participant_count']


