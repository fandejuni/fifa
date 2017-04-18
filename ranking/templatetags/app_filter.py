from django import template

register = template.Library()

@register.filter(name='decimal')
def decimal(x):
    return '{0:.1f}'.format(x)
