from django.db import models


class Category(models.Model):
    category_text = models.CharField(max_length=200, verbose_name='category text', name='')


class Label(models.Model):
    label_text = models.CharField(max_length=100, verbose_name='label text', name='')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Like(models.Model):
    like_text = models.CharField(max_length=10, verbose_name='like text')
    like_count = models.IntegerField(verbose_name='like count')


class Comment(models.Model):
    like = models.ForeignKey(Like, on_delete=models.CASCADE)
    comment_text = models.TextField(verbose_name='comment text')


class Post(models.Model):
    label = models.ManyToManyField(Label)
    category = models.ManyToManyField(Category)
    like = models.ForeignKey(Like, on_delete=models.CASCADE)
    post_head = models.CharField(max_length=200, verbose_name='post head')
    post_body = models.TextField(verbose_name='post body')
    post_date = models.DateField(verbose_name='post date')
    post_image = models.ImageField(verbose_name='post image')


class User(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, verbose_name='first name', name='')
    last_name = models.CharField(max_length=100, verbose_name='last name', name='')
    email = models.EmailField(verbose_name='email', name='')
    phone_number = models.IntegerField(verbose_name='phone number', name='')
    image = models.ImageField(verbose_name='image', name='')
