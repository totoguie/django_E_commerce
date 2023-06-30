from django import template
from babel.numbers import format_number

register = template.Library()

@register.filter
def format_with_spaces(value):
    return format_number(value, locale='fr')