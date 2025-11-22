from .models import Comment, Post
from django import forms

class CommentForm(forms.ModelForm):
    subscribe = forms.BooleanField(
        required=False,
        label="Subscribe to my newsletter",
        help_text="I consent to receiving email updates."
    )

    class Meta:
        model = Comment
        
        fields = ["email","full_name", "content", "subscribe"]

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'excerpt', 'category', 'featured_image', 'is_featured']
        
        