from django.urls import path
from . import views

app_name = 'posting'
urlpatterns = [
    path('', views.showPosts, name='showPosts'),
]
