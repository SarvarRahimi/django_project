from django import template

register = template.Library()


@register.filter(name='likeCounter')
def likeCounter(value, arg):
    return value.filter(type__exact=arg).count()

