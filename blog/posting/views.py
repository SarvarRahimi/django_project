# from django.http import HttpResponse
from django.shortcuts import render

from posting.models import Post


def showPosts(request):
    ordered_posts = Post.objects.order_by('-time')
    return render(request, 'posting/showPosts.html', {'posts': ordered_posts})

