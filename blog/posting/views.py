from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django.db.models import Q

from posting.models import Post, Label, PostLikes, BlogUser, Comment, CommentLikes, Category


def showPosts(request):
    if request.user.is_authenticated:
        if request.user.is_superuser or request.user.groups.filter(name__iexact='ویراستار').exists():
            all_posts = Post.objects.all()
        else:
            permitted_posts = Post.objects.all().filter(activated=True, permitted=True).order_by('-time')
            user_posts = Post.objects.filter(author__user__username__iexact=request.user.username)
            all_posts = permitted_posts.union(user_posts)
    else:
        all_posts = Post.objects.all().filter(activated=True, permitted=True).order_by('-time')
    return render(request, 'posting/showPosts.html', {'posts': all_posts, 'user': request.user})


def showPost(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user.is_authenticated:
        if request.user.is_superuser or request.user.groups.filter(name='ویراستار').exists():
            all_comments = Comment.objects.filter(post_id=post.id)
        else:
            all_comments = Comment.objects.all().filter(post_id=post.id, activated=True, permitted=True).order_by(
                '-time')
    else:
        all_comments = Comment.objects.all().filter(post_id=post.id, activated=True, permitted=True).order_by('-time')
    return render(request, 'posting/showPost.html', {'post': post, 'comments': all_comments, 'user': request.user})


def showPostByLabel(request, label_id):
    label = get_object_or_404(Label, pk=label_id)
    posts = Post.objects.all().filter(label__label_text__icontains=label.label_text)
    return render(request, 'posting/showPosts.html', {'posts': posts, 'user': request.user})


def showPostByCategory(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    posts = Post.objects.all().filter(category__category_text__icontains=category.category_text)
    return render(request, 'posting/showPosts.html', {'posts': posts, 'user': request.user})


def changePost(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    labels = Label.objects.all()
    categories = Category.objects.all()

    return render(request, 'posting/create.html',
                  {'labels': labels, 'categories': categories, 'user': request.user, 'post': post})


def createPosts(request):
    if request.POST:
        try:
            user = BlogUser.objects.get(user__username__iexact=request.user.username)
        except Exception as c:
            print('the user does not exist or not permitted: ', c)
            messages.add_message(request, messages.ERROR, 'شما برای ساخت پست مجاز نیستید')
            return HttpResponseRedirect(reverse('posting:showPosts'))

        try:
            category = Category.objects.get(category_text=request.POST['categoryBox'])
        except Exception as c:
            print('categoryError while creating post: ', c)
            category = Category.objects.create(category_text=request.POST['categoryBox'])

        try:
            image = request.FILES['imageBox']
        except Exception as c:
            print('imageError while creating post: ', c)
            messages.add_message(request, messages.ERROR, 'هیچ عکسی برای پست انتخاب نشده است')
            return redirect(request.META.get('HTTP_REFERER'))
            # return HttpResponseRedirect(reverse('posting:createPosts'))

        try:
            oldPostId = request.POST['old_post']
            newPost = get_object_or_404(Post, pk=oldPostId)
            newPost.category = category
            newPost.image = image
        except Exception as p:
            print('creatingPostError while creating post: ', p)
            newPost = Post.objects.create(author=user, category=category, image=image,
                                          summary=request.POST['summaryBox'], head=request.POST['headBox'],
                                          body=request.POST['bodyBox'])

        labelsInBack = request.POST.getlist('multiSelect')
        for label in labelsInBack:
            try:
                labelResult = Label.objects.get(label_text__iexact=label)
            except Exception as e:
                labelResult = Label.objects.create(label_text=label)
                print('labelError while creating post: ', e)
            newPost.label.add(labelResult)
        newPost.save()
        messages.add_message(request, messages.SUCCESS, 'پست با موفقیت ثبت شد')
        return HttpResponseRedirect(reverse('posting:showPosts'))
    else:
        labels = Label.objects.all()
        categories = Category.objects.all()
        return render(request, 'posting/create.html',
                      {'labels': labels, 'categories': categories, 'user': request.user})


def createComment(request, post_id):
    if request.POST:
        data = request.POST
        if not request.user.is_superuser:
            user = get_object_or_404(BlogUser, pk=request.user.id - 1)
        else:
            user = get_object_or_404(BlogUser, pk=request.user.id)
        post = get_object_or_404(Post, pk=post_id)
        newComment = Comment.objects.create(user=user, post=post, comment_text=data['comment'])
        newComment.save()
        messages.add_message(request, messages.SUCCESS, 'کامنت با موفقیت ایجاد شد')
        return redirect(reverse('posting:showPost', args=(post.id,)))
    else:
        raise Http404


@csrf_protect
def postLiking(request):
    # PostLikes.objects.all().delete()
    data = request.POST
    if not request.user.is_superuser:
        user = get_object_or_404(BlogUser, pk=request.user.id - 1)
    else:
        user = get_object_or_404(BlogUser, pk=request.user.id)
    post = get_object_or_404(Post, pk=data['post_id'])

    if data['status'] == 'True':
        typeLike = True
    else:
        typeLike = False

    try:
        postUserLike = PostLikes.objects.get(user=user, post=post)
        postUserLike.delete()
    except Exception as e:
        print('likeError while postLiking: ', e)
        newLike = PostLikes.objects.create(post=post, user=user, type=typeLike)
        newLike.save()

    return JsonResponse({'count': PostLikes.objects.filter(type=typeLike, post=post).count(), 'status': typeLike})


@csrf_protect
def commentLiking(request):
    data = request.POST
    if not request.user.is_superuser:
        user = get_object_or_404(BlogUser, pk=request.user.id - 1)
    else:
        user = get_object_or_404(BlogUser, pk=request.user.id)
    comment = get_object_or_404(Comment, pk=data['comment_id'])

    if data['status'] == 'True':
        typeLike = True
    else:
        typeLike = False

    try:
        commentUserLike = CommentLikes.objects.get(user=user, comment=comment)
        commentUserLike.delete()
    except Exception as e:
        print('likeError while commentLiking: ', e)
        newLike = CommentLikes.objects.create(comment=comment, user=user, type=typeLike)
        newLike.save()

    return JsonResponse(
        {'count': CommentLikes.objects.filter(type=typeLike, comment=comment).count(), 'status': typeLike})


def search(request):
    if request.POST:
        if request.POST.get('typeSearch') == 'simple':
            inputValue = request.POST['searchInput']
            posts = Post.objects.filter(
                Q(head__iregex=inputValue) | Q(body__iregex=inputValue) | Q(summary__iregex=inputValue) | Q(
                    label__label_text__iregex=inputValue) | Q(category__category_text__iregex=inputValue) | Q(
                    author__user__username__iregex=inputValue) | Q(
                    author__user__first_name__iregex=inputValue), activated=True, permitted=True).distinct()
            return render(request, 'posting/showPosts.html', {'posts': posts, 'user': request.user})

        elif request.POST.get('typeSearch') == 'advance':
            posts = Post.objects.filter(
                head__iregex=request.POST['headBox'], body__iregex=request.POST['bodyBox'],
                label__label_text__iregex=request.POST['labelBox'],
                author__user__username__iregex=request.POST['authorBox'],
                author__user__first_name__iregex=request.POST[
                    'authorBox'], activated=True, permitted=True).distinct()
            return render(request, 'posting/showPosts.html', {'posts': posts, 'user': request.user})

        else:
            all_posts = Post.objects.all().filter(activated=True, permitted=True).order_by('-time')
            return render(request, 'posting/showPosts.html', {'posts': all_posts, 'user': request.user})
    else:
        raise Http404


def changeActivation(request):
    if request.POST:
        if request.POST['button_state'] == 'activation':
            if request.POST['type_change'] == 'post':
                post = get_object_or_404(Post, pk=request.POST['post_id'])
                post.activated = not post.activated
                post.save()
                return JsonResponse({'button': 'activation', 'status': post.activated})
            else:
                comment = get_object_or_404(Comment, pk=request.POST['post_id'])
                comment.activated = not comment.activated
                comment.save()
                return JsonResponse({'button': 'activation', 'status': comment.activated})
        else:
            if request.POST['type_change'] == 'post':
                post = get_object_or_404(Post, pk=request.POST['post_id'])
                post.permitted = not post.permitted
                post.save()
                return JsonResponse({'button': 'permitted', 'status': post.permitted})
            else:
                comment = get_object_or_404(Comment, pk=request.POST['post_id'])
                comment.permitted = not comment.permitted
                comment.save()
                return JsonResponse({'button': 'permitted', 'status': comment.permitted})
    else:
        raise Http404


def creatingUser(request):
    if request.POST:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            if request.POST['password'] == request.POST['password2']:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password'],
                                                email=request.POST['email'])
                user.first_name = request.POST['firstName']
                user.last_name = request.POST['lastName']
                user.save()
                blogUser = BlogUser.objects.create(user=user, image=request.FILES['image'],
                                                   phone_number=request.POST['phone'])
                blogUser.save()
                messages.add_message(request, messages.SUCCESS, 'ثبت نام با موفقیت انجام شد')
                return HttpResponseRedirect(reverse('posting:showPosts'))
            else:
                messages.add_message(request, messages.ERROR, 'رمزها با هم یکسان نیستند')
                return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.add_message(request, messages.ERROR, 'کاربری با این مشخصات از قبل وجود دارد')
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        return render(request, 'posting/register.html')


def logOut(request):
    logout(request)
    messages.success(request, 'خروج با موفقیت انجام شد')
    return HttpResponseRedirect(reverse('posting:showPosts'))


def logIn(request):
    if request.POST:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            messages.add_message(request, messages.SUCCESS, 'ورود با موفقیت انجام شد')
            return HttpResponseRedirect(reverse('posting:showPosts'))
        else:
            messages.add_message(request, messages.ERROR, 'نام کاربری یا رمز عبور اشتباه است')
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        return render(request, 'posting/login.html')
