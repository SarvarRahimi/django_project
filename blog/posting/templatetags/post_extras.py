from django import template
# from math import floor
# from django.utils import timezone
register = template.Library()


@register.filter(name='likeCounter')
def likeCounter(value, arg):
    return value.filter(type__exact=arg).count()


# @register.filter(name='timeSince')
# def timeSince(value):
#     print(value - value, 'answer')
#     seconds = floor((timezone.now() - value) / 1000)
#
#     interval = seconds / 31536000
#     if interval > 1:
#         return f'{floor(interval)} سال قبل '
#
#     interval = seconds / 2592000
#     if interval > 1:
#         return f'{floor(interval)} ماه قبل '
#
#     interval = seconds / 86400
#     if interval > 1:
#         return f'{floor(interval)} روز قبل '
#
#     interval = seconds / 3600
#     if interval > 1:
#         return f'{floor(interval)} ساعت قبل '
#
#     interval = seconds / 60
#     if interval > 1:
#         return f'{floor(interval)} دقیقه قبل '
#
#     else:
#         return f'{floor(seconds)}  ثانیه قبل '
