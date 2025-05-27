from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return ''

@register.filter
def add(value, arg):
    try:
        return float(value) + float(arg)
    except:
        return value
