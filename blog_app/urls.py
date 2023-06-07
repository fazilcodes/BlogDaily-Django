from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name='home'),
    path('signup/', views.SignUp, name="signup"),
    path('profile/<str:pk>', views.Profile, name="profile"),
    path('post/<int:id>', views.Post, name="post"),
    path('blog/', views.Addblog, name='addblog'),
    path('addblogajax', views.AddBlog_Ajax, name='ajax')
]