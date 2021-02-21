from django.urls import path
from . import views

app_name = 'posting'
urlpatterns = [
    path('', views.showPosts, name='showPosts'),
    path('<int:label_id>/showPostByLabel/', views.showPostByLabel, name='showPostByLabel'),
    path('<int:post_id>/showPost/', views.showPost, name='showPost'),
    path('createPage/', views.showCreatePostsPage, name='showCreatePostsPage'),
    path('create/', views.createPosts, name='createPosts'),
    path('postLiking/', views.postLiking, name='postLiking')
]
