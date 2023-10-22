from urllib import parse

from django import template


register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={'class': css})


@register.filter
def multiply(value, arg):
    return value * arg


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    query = context['request'].GET.copy()
    query.update(kwargs)
    return parse.urlencode(query)
