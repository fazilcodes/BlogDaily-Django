from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name='home'),
    path('signup/', views.SignUp, name="signup"),
    path('signin/', views.Signin, name="signin"),
    path('logout/', views.Logout, name="logout"),
    path('profile/<str:pk>', views.Profile, name="profile"),
    path('post/<int:id>', views.Post, name="post"),
    path('blog/', views.Addblog, name='addblog'),
    path('addblogajax', views.AddBlog_Ajax, name='ajax'),
    path('updateblog/<int:id>', views.Updateblog, name="updateblog"),
    path('updateprofile/<int:id>', views.Updateprofile, name='updateprofile'),
    path('category/<str:pk>', views.Category_posts, name='category'),
    path('search/', views.Search, name='search')
]