
from django import template
from django.utils.safestring import mark_safe
register = template.Library()

@register.simple_tag
def display_users():
    return 'abctest'