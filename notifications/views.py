# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render
# from .models import Notification

# @login_required
# def my_notifications(request):
#       notifications = request.user.notifications.order_by('-timestamp')
#       notifications.filter(unread=True).update(unread=False)
#       return render(request, 'notifications/my_notifications.html', {'notifications': notifications})

# from django.shortcuts import render
# from .models import Notification

# def my_notifications(request):
#     notifications = Notification.objects.filter(recipient=request.user).order_by('-timestamp')
#     return render(request, 'notifications/my_notifications.html', {
#         'notifications': notifications,
#     })


# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render
# from .models import Notification

# @login_required
# def notifications_view(request):
#     notifications = Notification.objects.filter(recipient=request.user).order_by('-timestamp')
#     unread_count = notifications.filter(unread=True).count()
#     return render(request, 'notifications/my_notifications.html', {
#         'notifications': notifications,
#         'unread_count': unread_count,
#     })

# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render
# from .models import Notification

# @login_required
# def my_notifications(request):
#     notifications = Notification.objects.filter(recipient=request.user).order_by('-timestamp')
#     unread_count = notifications.filter(unread=True).count()
#     notifications.filter(unread=True).update(unread=False)
#     return render(request, 'notifications/my_notifications.html', {
#         'notifications': notifications,
#         'unread_count': 0,
#     })


# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render
# from .models import Notification

# @login_required
# def my_notifications(request):
#     notifications = Notification.objects.filter(recipient=request.user).order_by('-timestamp')

#     unread_notifications = notifications.filter(unread=True)
#     unread_count = unread_notifications.count()
#     # unread notification গুলোকে পড়া হিসেবে চিহ্নিত করো
#     unread_notifications.update(unread=False)

#     return render(request, 'notifications/my_notifications.html', {
#         'notifications': notifications,
#         'unread_count': unread_count,
#     })

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Notification

@login_required
def my_notifications(request):
    notifications = Notification.objects.filter(recipient=request.user).order_by('-timestamp')
    unread_count = notifications.filter(unread=True).count()

    return render(request, 'notifications/my_notifications.html', {
        'notifications': notifications,
        'unread_count': unread_count,
    })

@login_required
def notification_redirect(request, pk):
    notification = get_object_or_404(Notification, pk=pk, recipient=request.user)
    if notification.unread:
        notification.unread = False
        notification.save()

    if notification.url:
        return redirect(notification.url)
    else:
        return redirect(reverse('my_notifications'))
