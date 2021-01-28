# from django.utils import timezone
from django.db import models


class Category(models.Model):
    category_text = models.CharField(max_length=200, verbose_name='category text', name='')

    def __str__(self):
        return self.category_text


class Label(models.Model):
    label_text = models.CharField(max_length=100, verbose_name='label text', name='')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.label_text


class Like(models.Model):
    like_text = models.CharField(max_length=10, verbose_name='like text', name='')
    like_count = models.IntegerField(verbose_name='like count', name='')
    like_date = models.DateTimeField(verbose_name='like date', name='', default='2021-01-28')

    def __str__(self):
        return self.like_count


class Comment(models.Model):
    like = models.ForeignKey(Like, on_delete=models.CASCADE)
    comment_text = models.TextField(verbose_name='comment text', name='')
    date = models.DateTimeField(verbose_name='comment date', name='', default='2021-01-28')

    def __str__(self):
        return self.comment_text


class Post(models.Model):
    label = models.ManyToManyField(Label)
    category = models.ManyToManyField(Category)
    like = models.ForeignKey(Like, on_delete=models.CASCADE)
    head = models.CharField(max_length=200, verbose_name='post head')
    body = models.TextField(verbose_name='post body')
    date = models.DateTimeField(verbose_name='post date', name='', default='2021-01-28')
    image = models.ImageField(verbose_name='post image')

    def __str__(self):
        main_post = f'{self.head} \n {self.body}'
        return main_post


class User(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, verbose_name='first name', name='')
    last_name = models.CharField(max_length=100, verbose_name='last name', name='')
    email = models.EmailField(verbose_name='email', name='')
    phone_number = models.IntegerField(verbose_name='phone number', name='')
    image = models.ImageField(verbose_name='image', name='')

    def __str__(self):
        return f"first name:{self.first_name}\nlast name:{self.last_name}\nemail:{self.email}"
