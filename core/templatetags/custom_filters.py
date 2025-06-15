from django import template

register = template.Library()

@register.filter
def get_attr(obj, attr):
    return [getattr(item, attr) for item in obj]

@register.filter(name='get_item')
def get_item(dictionary, key):
    """
    Template filter to get an item from a dictionary using bracket notation
    Usage: {{ mydict|get_item:item_key }}
    """
    return dictionary.get(str(key), dictionary.get(key, None))