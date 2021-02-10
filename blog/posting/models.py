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
    image = models.ImageField(verbose_name='عکس', upload_to='media/user/%Y/%m/%d/', blank=True)

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"

    def __str__(self):
        return f"{self.user}"


class Comment(models.Model):
    user = models.ForeignKey(BlogUser, on_delete=models.CASCADE, verbose_name='کاربر', null=True)
    comment_text = models.TextField(verbose_name='عنوان', editable=False)
    time = models.DateTimeField(verbose_name='زمان', default=timezone.now)
    like = models.BooleanField(verbose_name='لایک', default=False)
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
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, verbose_name='کامنت', null=True)
    head = models.CharField(max_length=200, verbose_name='تیتر')
    body = models.TextField(verbose_name='متن')
    summary = models.CharField(max_length=200, verbose_name='خلاصه', blank=True)
    time = models.DateTimeField(verbose_name='زمان', default=timezone.now)
    image = models.ImageField(verbose_name='عکس', upload_to='media/%Y/%m/%d/', blank=True)
    like = models.BooleanField(verbose_name='لایک', default=False)
    permission = models.BooleanField(verbose_name='اجازه نمایش', default=False)
    activated = models.BooleanField(verbose_name='وضعیت فعال بودن', default=False)

    class Meta:
        verbose_name = "پست"
        verbose_name_plural = "پست ها"

    def __str__(self):
        main_post = f'{self.head} \n {self.body}'
        return main_post


class PostLikes(models.Model):
    user = models.ForeignKey(BlogUser, on_delete=models.CASCADE, verbose_name='کاربر', null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='پست')
    type = models.BooleanField(verbose_name='نوع')

    class Meta:
        verbose_name = "لایک پست"
        verbose_name_plural = "لایک های پست"

    def __str__(self):
        return f'{self.user} \n {self.post}\n like type: {type}'


class CommentLikes(models.Model):
    user = models.ForeignKey(BlogUser, on_delete=models.CASCADE, verbose_name='کاربر', null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='پست')
    type = models.BooleanField(verbose_name='نوع')

    class Meta:
        verbose_name = "لایک کامنت"
        verbose_name_plural = "لایک های کامنت"

    def __str__(self):
        return f'{self.user} \n {self.post}\n like type: {type}'
