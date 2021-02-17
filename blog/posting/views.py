# from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from posting.models import Post, Label


def showPosts(request):
    all_posts = Post.objects.all().filter(activated=True, permission=True).order_by('-time')
    return render(request, 'posting/showPosts.html', {'posts': all_posts})


def showPost(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'posting/showPost.html', {'post': post})


def showCreatePostsPage(request):
    return render(request, 'posting/create.html')


def showPostByLabel(request, label_id):
    label = get_object_or_404(Label, pk=label_id)
    posts = Post.objects.all().filter(label__label_text__icontains=label.label_text)
    return render(request, 'posting/showPosts.html', {'posts': posts})


def createPosts(request):
    if request.POST:
        newPost = Post.objects.create(author=request.POST['authorBox'], label=request.POST['labelBox'],
                                      image=request.POST['imageBox'], category=request.POST['categoryBox'],
                                      summary=request.POST['summaryBox'], head=request.POST['headBox'],
                                      body=request.POST['bodyBox'])
        newPost.save()
        return render(request, 'posting/showPosts.html')
