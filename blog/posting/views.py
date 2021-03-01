# from django.http import HttpResponse
# from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django.db.models import Q

from posting.models import Post, Label, PostLikes, BlogUser, Comment, CommentLikes, Category


def showPosts(request):
    if request.user.is_authenticated:
        all_posts = Post.objects.all()
    else:
        all_posts = Post.objects.all().filter(activated=True, permitted=True).order_by('-time')
    return render(request, 'posting/showPosts.html', {'posts': all_posts, 'user': request.user})


def showPost(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = Comment.objects.all().filter(post_id=post.id, activated=True, permitted=True).order_by('-time')
    # print(comments[0].commentlikes_set.filter(type__exact=True).count())
    # print(comments[0].commentlikes_set.filter(type__exact=False).count())
    return render(request, 'posting/showPost.html', {'post': post, 'comments': comments})


def showCreatePostsPage(request):
    labels = Label.objects.all()
    categories = Category.objects.all()
    return render(request, 'posting/create.html', {'labels': labels, 'categories': categories})


def showPostByLabel(request, label_id):
    label = get_object_or_404(Label, pk=label_id)
    posts = Post.objects.all().filter(label__label_text__icontains=label.label_text)
    return render(request, 'posting/showPosts.html', {'posts': posts})


def createPosts(request):
    if request.POST:
        user = get_object_or_404(BlogUser, pk=request.user.id)
        try:
            category = Category.objects.get(category_text=request.POST['categoryBox'])
        except Exception as c:
            print(c)
            category = Category.objects.create(category_text=request.POST['categoryBox'])
        newPost = Post.objects.create(author=user,
                                      image=request.POST['imageBox'], category=category,
                                      summary=request.POST['summaryBox'], head=request.POST['headBox'],
                                      body=request.POST['bodyBox'])

        labelsInBack = [label for label in request.POST.get("labelsBox")]
        for label in labelsInBack:
            try:
                labelResult = Label.objects.get(label_text__iregex=label)
            except Exception as e:
                labelResult = Label.objects.create(label_text=label)
                print(e)
            newPost.label.add(labelResult)
        newPost.save()

        all_posts = Post.objects.all().filter(activated=True, permitted=True).order_by('-time')
        return render(request, 'posting/showPosts.html', {'posts': all_posts})


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
    # PostLikes.objects.all().delete()
    data = request.POST
    user = get_object_or_404(BlogUser, pk=request.user.id)
    post = get_object_or_404(Post, pk=data['post_id'])

    if data['status'] == 'True':
        typeLike = True
    else:
        typeLike = False

    try:
        postUserLike = PostLikes.objects.get(user=user)
        postUserLike.delete()
    except Exception as e:
        print(e)
        newLike = PostLikes.objects.create(post=post, user=user, type=typeLike)
        newLike.save()

    return JsonResponse({'count': PostLikes.objects.filter(type=typeLike).count(), 'status': typeLike})


@csrf_protect
def commentLiking(request):
    data = request.POST
    user = get_object_or_404(BlogUser, pk=request.user.id)
    comment = get_object_or_404(Comment, pk=data['comment_id'])

    if data['status'] == 'True':
        typeLike = True
    else:
        typeLike = False

    try:
        commentUserLike = CommentLikes.objects.get(user_id=int(data['user_id']))
        commentUserLike.delete()
    except Exception as e:
        print(e)
        newLike = CommentLikes.objects.create(comment=comment, user=user, type=typeLike)
        newLike.save()

    return JsonResponse({'count': CommentLikes.objects.filter(type=typeLike).count(), 'status': typeLike})


def search(request):
    if request.POST:
        if request.POST['searchInput']:
            inputValue = request.POST['searchInput']
            posts = Post.objects.filter(
                Q(head__iregex=inputValue) | Q(body__iregex=inputValue) | Q(summary__iregex=inputValue) | Q(
                    label__label_text__iregex=inputValue) | Q(category__category_text__iregex=inputValue) | Q(
                    author__user__username__iregex=inputValue) | Q(
                    author__user__first_name__iregex=inputValue)).distinct()
            return render(request, 'posting/showPosts.html', {'posts': posts})

        elif request.POST['authorBox'] or request.POST['headBox'] or request.POST['bodyBox'] or \
                request.POST['labelBox']:
            posts = Post.objects.filter(
                Q(head__iregex=request.POST['headBox']) | Q(body__iregex=request.POST['bodyBox']) | Q(
                    label__label_text__iregex=request.POST['labelBox']) | Q(
                    author__user__username__iregex=request.POST['authorBox']) | Q(
                    author__user__first_name__iregex=request.POST['authorBox'])).distinct()
            return render(request, 'posting/showPosts.html', {'posts': posts})

        else:
            all_posts = Post.objects.all().filter(activated=True, permitted=True).order_by('-time')
            return render(request, 'posting/showPosts.html', {'posts': all_posts})


def advancedSearch(request):
    if request.POST:
        if request.POST['authorBox'] or request.POST['headBox'] or request.POST['bodyBox'] or \
                request.POST['labelBox']:
            posts = Post.objects.filter(
                Q(head__iregex=request.POST['headBox']) | Q(body__iregex=request.POST['bodyBox']) | Q(
                    label__label_text__iregex=request.POST['labelBox']) | Q(
                    author__user__username__iregex=request.POST['authorBox']) | Q(
                    author__user__first_name__iregex=request.POST['authorBox'])).distinct()
            return render(request, 'posting/showPosts.html', {'posts': posts})

        else:
            all_posts = Post.objects.all().filter(activated=True, permitted=True).order_by('-time')
            return render(request, 'posting/showPosts.html', {'posts': all_posts})


def changeActivation(request):
    if request.POST:
        if request.POST['button_state'] == 'activation':
            post = get_object_or_404(Post, pk=request.POST['post_id'])
            post.activated = not post.activated
            post.save()
            return JsonResponse({'button': 'activation', 'status': post.activated})
        else:
            post = get_object_or_404(Post, pk=request.POST['post_id'])
            post.permitted = not post.permitted
            post.save()
            return JsonResponse({'button': 'permitted', 'status': post.permitted})
