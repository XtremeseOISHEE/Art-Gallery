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

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Notification

@login_required
def my_notifications(request):
    notifications = Notification.objects.filter(recipient=request.user).order_by('-timestamp')
    unread_count = notifications.filter(unread=True).count()
    notifications.filter(unread=True).update(unread=False)
    return render(request, 'notifications/my_notifications.html', {
        'notifications': notifications,
        'unread_count': 0,
    })
