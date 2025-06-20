from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Message
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def inbox(request):
    # Show distinct users who sent messages + count unread per sender
    received_msgs = Message.objects.filter(receiver=request.user)
    # Group by sender and count unread
    senders = {}
    for msg in received_msgs:
        sender = msg.sender
        if sender not in senders:
            senders[sender] = {'unread': 0, 'last_msg': None}
        if not msg.is_read:
            senders[sender]['unread'] += 1
        # Save last message timestamp for sorting
        if senders[sender]['last_msg'] is None or msg.timestamp > senders[sender]['last_msg']:
            senders[sender]['last_msg'] = msg.timestamp

    # Sort senders by last message time descending
    sorted_senders = sorted(senders.items(), key=lambda x: x[1]['last_msg'], reverse=True)

    return render(request, 'messaging/inbox.html', {
        'senders': sorted_senders
    })

@login_required
def send_message(request, username):
    receiver = get_object_or_404(User, username=username)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(sender=request.user, receiver=receiver, content=content)
            return redirect('conversation_detail', username=receiver.username)
    return render(request, 'messaging/send_message.html', {'receiver': receiver})

from django.db.models import Q

@login_required
def conversation_detail(request, username):
    other_user = get_object_or_404(User, username=username)
    
    messages = Message.objects.filter(
        (Q(sender=request.user) & Q(receiver=other_user)) |
        (Q(sender=other_user) & Q(receiver=request.user))
    ).order_by('timestamp')

    # Mark unread messages as read
    messages.filter(receiver=request.user, is_read=False).update(is_read=True)

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(sender=request.user, receiver=other_user, content=content)
            return redirect('conversation_detail', username=other_user.username)

    return render(request, 'messaging/conversation_detail.html', {
        'messages': messages,
        'other_user': other_user
    })
