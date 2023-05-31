from django.db import models
from django.contrib.auth import get_user_model



# This is a reference to the user model created using Django build in User model
User = get_user_model()
# -------------------------------------------------------------------

# Create your models here.
# ------------------------------------------------------------------------------------------------


class UserProfileDB(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_id = models.IntegerField()
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to="Profile_Pictures", blank=True, default="default_profile.png")
    profession = models.CharField(max_length=200, blank=True)
    