from django.db import models
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField



# This is a reference to the user model created using Django build in User model
User = get_user_model()
# -------------------------------------------------------------------

# Create your models here.
# ------------------------------------------------------------------------------------------------


class UserProfileDB(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to="Profile_Pictures", blank=True, default="default_profile.png")
    profession = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self) -> str:
        return self.user.get_username()


class BlogPostDB(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    body = RichTextField(blank=True, null=True)
    blog_date = models.DateField(auto_now_add=True)
    category = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.author