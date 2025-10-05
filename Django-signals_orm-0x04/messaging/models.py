from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    edited = models.BooleanField(default=False)
    edited_by = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, related_name="edited_messages"
    )

    # Self-referential FK for threaded replies
    parent_message = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replies'
    )

    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username}"

    def get_thread(self):
        """
        Recursively fetch all replies to this message in threaded order.
        """
        thread = []
        replies = self.replies.all().select_related('sender', 'receiver').prefetch_related('replies')

        for reply in replies:
            thread.append(reply)
            thread.extend(reply.get_thread())  # recursion to get nested replies

        return thread

    @classmethod
    def get_conversation(cls, user1, user2):
        """
        Retrieve all messages exchanged between two users, optimizing related queries.
        """
        messages = cls.objects.filter(
            models.Q(sender=user1, receiver=user2) | models.Q(sender=user2, receiver=user1)
        ).select_related('sender', 'receiver', 'parent_message').prefetch_related('replies')

        return messages.order_by('timestamp')


class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="history")
    old_content = models.TextField()
    edited_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    edited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Edit history for message {self.message.id}"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="notifications")
    text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.text}"
