from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    category_text = models.CharField(max_length=200, verbose_name='عنوان')

    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"

    def __str__(self):
        return self.category_text


class Label(models.Model):
    label_text = models.CharField(max_length=100, verbose_name='عنوان')

    class Meta:
        verbose_name = "برچسب"
        verbose_name_plural = "برچسب ها"

    def __str__(self):
        return self.label_text


class BlogUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='کاربر')
    email = models.EmailField(verbose_name='ایمیل', name='email')
    phone_number = models.IntegerField(verbose_name='شماره موبایل')
    image = models.ImageField(verbose_name='عکس')

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"

    def __str__(self):
        return f"{self.user}"


class Comment(models.Model):
    user = models.ForeignKey(BlogUser, on_delete=models.CASCADE, verbose_name='کاربر', null=True)
    like = models.BooleanField(verbose_name='لایک', default=False)
    comment_text = models.TextField(verbose_name='عنوان')
    time = models.DateTimeField(verbose_name='زمان', default=timezone.now)
    permission = models.BooleanField(verbose_name='اجازه نمایش', default=False)
    activated = models.BooleanField(verbose_name='وضعیت فعال بودن', default=False)

    class Meta:
        verbose_name = "کامنت"
        verbose_name_plural = "کامنت ها"

    def __str__(self):
        return self.comment_text


class Post(models.Model):
    author = models.ForeignKey(BlogUser, on_delete=models.CASCADE, verbose_name='نویسنده', null=True)
    label = models.ManyToManyField(Label, verbose_name='برچسب')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='دسته بندی', null=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, verbose_name='کامنت')
    like = models.BooleanField(verbose_name='لایک', default=False)
    head = models.CharField(max_length=200, verbose_name='تیتر')
    body = models.TextField(verbose_name='متن')
    time = models.DateTimeField(verbose_name='زمان', default=timezone.now)
    image = models.ImageField(verbose_name='عکس')
    permission = models.BooleanField(verbose_name='اجازه نمایش', default=False)
    activated = models.BooleanField(verbose_name='وضعیت فعال بودن', default=False)

    class Meta:
        verbose_name = "پست"
        verbose_name_plural = "پست ها"

    def __str__(self):
        main_post = f'{self.head} \n {self.body}'
        return main_post
