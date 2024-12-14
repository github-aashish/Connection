from django import template
from ..models import *

register = template.Library()

@register.filter(name='check')
def check(postUser, AuthUser):
    try:
        following = Follower.objects.get(user=postUser)
    except:
        return False
    
    if AuthUser in following.followers.all():
        return True
    else:
        return False
    