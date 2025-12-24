from .models import Comment, Post
from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget


class CommentForm(forms.ModelForm):
    subscribe = forms.BooleanField(
        required=False,
        label="Subscribe to my newsletter",
        help_text="I consent to receiving email updates."
    )
    content = forms.CharField()
    

    class Meta:
        model = Comment
        
        fields = ["email","full_name", "content", "subscribe"]
        widgets = {'content': CKEditor5Widget( attrs={'class': 'django_ckeditor_5'}, config_name='default' ) }

class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'featured_image']
        
        