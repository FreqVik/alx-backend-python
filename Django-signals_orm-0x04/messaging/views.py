from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from .models import Message

@cache_page(60)
@login_required
def conversation_view(request, receiver_id):
    """
    Display a threaded conversation between the logged-in user and another user.
    Cached for 60 seconds using cache_page.
    Optimized with select_related and prefetch_related.
    """
    messages = Message.objects.filter(
        sender=request.user,
        receiver_id=receiver_id
    ).select_related('sender', 'receiver', 'parent_message').prefetch_related('replies')

    received = Message.objects.filter(
        sender_id=receiver_id,
        receiver=request.user
    ).select_related('sender', 'receiver', 'parent_message').prefetch_related('replies')

    all_messages = messages.union(received).order_by('timestamp')

    context = {"conversation": all_messages}
    return render(request, "messaging/conversation.html", context)


@login_required
def message_thread_view(request, message_id):
    """
    Fetch a single message and all its threaded replies recursively.
    """
    message = get_object_or_404(
        Message.objects.select_related('sender', 'receiver').prefetch_related('replies'),
        id=message_id
    )
    thread = message.get_thread()
    return render(request, "messaging/thread.html", {"message": message, "thread": thread})


@login_required
def unread_messages_view(request):
    """
    Display only unread messages for the logged-in user.
    Uses the custom manager and optimized query with `.only()`.
    """
    unread_messages = Message.unread.unread_for_user(request.user).only("sender", "receiver", "content", "timestamp")
    return render(request, "messaging/unread_inbox.html", {"unread_messages": unread_messages})
