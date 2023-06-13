from django.db import models
from django.contrib.auth import get_user_model




# This is a reference to the user model created using Django build in User model
User = get_user_model()
# -------------------------------------------------------------------

# Create your models here.
# ------------------------------------------------------------------------------------------------


class UserProfileDB(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profil_name = models.CharField(max_length=200, null=True, blank=True)
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to="Profile_Pictures", blank=True, default="default_profile.png")
    profession = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self) -> str:
        return self.user.get_username()


class BlogPostDB(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    author_profile = models.ForeignKey(UserProfileDB, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=200)
    blog_image = models.ImageField(upload_to="Post-Images", null=True, blank=True)
    caption = models.TextField(blank=True)
    blog_date = models.DateField(auto_now_add=True)
    category = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.author.get_username()


class CommentsDB(models.Model):
    post = models.ForeignKey(BlogPostDB, on_delete=models.CASCADE)
    commented_by = models.ForeignKey(UserProfileDB, on_delete=models.CASCADE)
    comment = models.TextField()
    commented_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.commented_by.user.username}: {self.comment[:10]}'