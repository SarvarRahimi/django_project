from django import template

from posting.models import Post, Comment

register = template.Library()


@register.filter(name='postLikeCounter')
def postLikeCounter(value, arg):
    post = Post.objects.get(pk=value)
    return post.postlikes_set.filter(type__exact=arg).count()


@register.filter(name='commentLikeCounter')
def commentLikeCounter(value, arg):
    comment = Comment.objects.get(pk=value)
    return comment.commentlikes_set.filter(type__exact=arg).count()


@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()
