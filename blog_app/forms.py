from django import forms
from django.forms import ModelForm
from .models import BlogPostDB


# Create model forms here
# -------------------------------------


class BlogForm(ModelForm):
    class Meta:
        model = BlogPostDB
        fields = ('title', 'body', 'category')