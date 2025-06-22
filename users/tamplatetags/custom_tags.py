from django import template
from django.contrib.auth import get_user_model

register = template.Library()

@register.simple_tag
def get_admin_user():
    User = get_user_model()
    return User.objects.filter(is_superuser=True).first()
