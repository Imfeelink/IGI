from django import template

register = template.Library()


@register.filter
def ddmmyyyy(value):
    if not value:
        return ''
    if hasattr(value, 'strftime'):
        return value.strftime('%d/%m/%Y')
    return value
