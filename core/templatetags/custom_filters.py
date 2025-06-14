from django import template

register = template.Library()

@register.filter
def get_attr(obj, attr):
    return [getattr(item, attr) for item in obj]