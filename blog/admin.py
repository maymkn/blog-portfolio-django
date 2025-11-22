from django.contrib import admin
from .models import Post, Comment, Category, NewsletterSubscriber

# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(NewsletterSubscriber)
admin.site.register(Category)