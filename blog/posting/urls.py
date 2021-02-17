from django.urls import path
from . import views

app_name = 'posting'
urlpatterns = [
    path('', views.showPosts, name='showPosts'),
    path('showPost', views.showPost, name='showPost'),
    path('createPage/', views.showCreatePostsPage, name='showCreatePostsPage'),
    path('create/', views.createPosts, name='createPosts')
]
