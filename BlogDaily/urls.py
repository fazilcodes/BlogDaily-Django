from django.contrib import admin
from django.urls import path, include
import blog_app.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("blog_app.urls")),
]
