from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    """Form for the image model"""
    class Meta:
        model = Post
        fields = ('title', 'body', 'excerpt', 'avatar', 'category', 'tags', 'author')
