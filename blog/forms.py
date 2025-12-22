from .models import Comment, Post
from django import forms
from ckeditor.widgets import CKEditorWidget

class CommentForm(forms.ModelForm):
    subscribe = forms.BooleanField(
        required=False,
        label="Subscribe to my newsletter",
        help_text="I consent to receiving email updates."
    )
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Comment
        
        fields = ["email","full_name", "content", "subscribe"]

class PostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'featured_image']
        
        