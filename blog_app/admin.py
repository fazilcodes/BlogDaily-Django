from django.contrib import admin
from .models import UserProfileDB, BlogPostDB, CommentsDB


# Register your models here.

admin.site.register(UserProfileDB)
admin.site.register(BlogPostDB)
admin.site.register(CommentsDB)