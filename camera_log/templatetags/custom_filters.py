from django import template

register = template.Library()

@register.filter
def status_class(status):
    if status == 'AI not working':
        return 'text-danger'
    elif status == 'Camera inactive':
        return 'text-warning'
    return ''
