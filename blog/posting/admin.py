from django.contrib import admin
from .models import Category, Comment, Post, Label, BlogUser, PostLikes, CommentLikes

admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Post)
admin.site.register(Label)
admin.site.register(BlogUser)
admin.site.register(PostLikes)
admin.site.register(CommentLikes)
