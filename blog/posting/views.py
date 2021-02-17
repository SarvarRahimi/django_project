# from django.http import HttpResponse
from django.shortcuts import render
from posting.models import Post


def showPosts(request):
    all_posts = Post.objects.all().filter(activated=True, permission=True).order_by('-time')
    return render(request, 'posting/showPosts.html', {'posts': all_posts})


def showCreatePostsPage(request):
    return render(request, 'posting/create.html')


def showPost(request):
    return render(request, 'posting/showPost.html')


def createPosts(request):
    if request.POST:
        newPost = Post.objects.create(author=request.POST['authorBox'], label=request.POST['labelBox'],
                                      image=request.POST['imageBox'], category=request.POST['categoryBox'],
                                      summary=request.POST['summaryBox'], head=request.POST['headBox'],
                                      body=request.POST['bodyBox'])
        newPost.save()
        return render(request, 'posting/showPosts.html')
