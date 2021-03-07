from django import template
register = template.Library()


@register.filter(name='likeCounter')
def likeCounter(value, arg):
    return value.filter(type__exact=arg).count()


@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()
