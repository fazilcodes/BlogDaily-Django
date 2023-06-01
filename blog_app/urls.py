from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name='home'),
    path('signup', views.SignUp, name="signup"),
    path('profile', views.Profile, name="profile"),
    path('post', views.Post, name="post"),
    path('blog', views.Addblog, name='addblog')
]