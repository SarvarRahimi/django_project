from django.urls import path
from . import views

app_name = 'posting'
urlpatterns = [
    path('', views.showPosts, name='showPosts'),
    path('<int:label_id>/showPostByLabel/', views.showPostByLabel, name='showPostByLabel'),
    path('<int:category_id>/showPostByCategory/', views.showPostByCategory, name='showPostByCategory'),
    path('<int:post_id>/showPost/', views.showPost, name='showPost'),
    path('create/', views.createPosts, name='createPosts'),
    path('postLiking/', views.postLiking, name='postLiking'),
    path('<int:post_id>/creatComments/', views.createComment, name='createComments'),
    path('commentLiking/', views.commentLiking, name='commentLiking'),
    path('search/', views.search, name='search'),
    path('advancedSearch/', views.advancedSearch, name='advancedSearch'),
    path('changeActivation/', views.changeActivation, name='changeActivation'),
    path('logOut/', views.logOut, name='logOut'),
    path('creatingUser/', views.creatingUser, name='creatingUser'),
    path('logIn/', views.logIn, name='logIn'),
]
