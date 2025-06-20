def unread_notifications(request):
    if request.user.is_authenticated:
        count = request.user.notifications.filter(unread=True).count()
        return {'unread_notification_count': count}
    return {}
