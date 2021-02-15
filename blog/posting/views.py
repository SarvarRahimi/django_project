# from django.http import HttpResponse
from django.shortcuts import render
from posting.models import Post


def showPosts(request):
    ordered_posts = Post.objects.order_by('-time')
    # contents = {'list_post': []}
    # for post in ordered_posts:
    #     contents['list_post'].append({
    #         'author': post.author,
    #         'labels': [label for label in post.label.all()],
    #         'head': post.head,
    #         'summary': post.summary,
    #         'time': post.time,
    #         'image': post.image,
    #         'like': post.postlikes_set.filter(type__exact=True).count(),
    #         'dislike': post.postlikes_set.filter(type__exact=False).count()
    #     })
    # for post in ordered_posts:
    #     print(post)
    return render(request, 'posting/showPosts.html', {'posts': ordered_posts, })
