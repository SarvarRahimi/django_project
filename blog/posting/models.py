# from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    category_text = models.CharField(max_length=200, verbose_name='category text', name='')

    def __str__(self):
        return self.category_text


class Label(models.Model):
    label_text = models.CharField(max_length=100, verbose_name='label text', name='')

    def __str__(self):
        return self.label_text


class BlogUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='', name='')
    email = models.EmailField(verbose_name='email', name='')
    phone_number = models.IntegerField(verbose_name='phone number', name='')
    image = models.ImageField(verbose_name='image', name='')

    def __str__(self):
        return f"{self.user}"


class Comment(models.Model):
    user = models.ForeignKey(BlogUser, on_delete=models.CASCADE, verbose_name='', name='')
    like = models.BooleanField(verbose_name='comment_like', name='', default=False)
    comment_text = models.TextField(verbose_name='comment text', name='')
    time = models.DateTimeField(verbose_name='comment date', name='', default='2021-01-28')

    def __str__(self):
        return self.comment_text


class Post(models.Model):
    user = models.ForeignKey(BlogUser, on_delete=models.CASCADE, verbose_name='', name='')
    label = models.ManyToManyField(Label)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='', name='')
    like = models.BooleanField(verbose_name='comment_like', name='', default=False)
    head = models.CharField(max_length=200, verbose_name='post head')
    body = models.TextField(verbose_name='post body')
    time = models.DateTimeField(verbose_name='post date', name='')
    image = models.ImageField(verbose_name='post image')

    def __str__(self):
        main_post = f'{self.head} \n {self.body}'
        return main_post
