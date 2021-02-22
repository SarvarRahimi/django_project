# from django.http import HttpResponse
# from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect

from posting.models import Post, Label, PostLikes, BlogUser, Comment


def showPosts(request):
    all_posts = Post.objects.all().filter(activated=True, permission=True).order_by('-time')
    return render(request, 'posting/showPosts.html', {'posts': all_posts})


def showPost(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = Comment.objects.all().filter(post_id=post.id, activated=True, permitted=True).order_by('-time')
    return render(request, 'posting/showPost.html', {'post': post, 'comments': comments})


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


def createComment(request, post_id):
    if request.POST:
        data = request.POST
        user = get_object_or_404(BlogUser, pk=request.user.id)
        post = get_object_or_404(Post, pk=post_id)
        newComment = Comment.objects.create(user=user, post=post, comment_text=data['comment'])
        newComment.save()
        # print('this part is done', post, 'the username is')
        return HttpResponseRedirect(reverse('posting:showPost', args=(post.id,)))
        # return render(request, 'posting/showPost.html', {'post': post})


@csrf_protect
def postLiking(request):
    data = request.POST
    user = get_object_or_404(BlogUser, pk=data['user_id'])
    post = get_object_or_404(Post, pk=data['post_id'])

    if data['status'] == 'True':
        typeLike = True
    else:
        typeLike = False

    try:
        postUserLike = PostLikes.objects.get(user_id=int(data['user_id']))
        postUserLike.delete()
    except Exception as e:
        print(e)
        newLike = PostLikes.objects.create(post=post, user=user, type=typeLike)
        newLike.save()

    return JsonResponse({'count': PostLikes.objects.filter(type=typeLike).count(), 'status': typeLike})
