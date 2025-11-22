from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)


    def __str__(self):
        return self.name
    
class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    excerpt = models.TextField(max_length=300, null=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    featured_image = models.ImageField(upload_to='blog/', default='blog/blog_default.jpg', blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'slug': self.slug})

class Comment(models.Model):
    post = models.ForeignKey(Post, blank=False, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField(blank=False, null=False)
    full_name = models.TextField(null=False, blank=False, max_length=30)
    email = models.EmailField(null=False, blank=False)
    created_date = models.DateTimeField(auto_now_add=True)

    

class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100, blank=True)
    subscribed_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.email
    


    """
    <!-- Blog Post 1 -->
    {%  for post in posts[4] %}
    
                <div class="blog-card" data-category="{{post.categories[0]}}" data-search="future education leadership trends">
                    <a href="#" class="blog-card-link">
                        <div class="card-image-container">
                            <img src="{{photo.featured_image.url}}" 
                                 alt="Leadership in education" class="card-image">
                            <div class="image-overlay"></div>
                        </div>
                        <div class="card-content">
                            <span class="category-badge">{{post.categories[0]}}</span>
                            <h3 class="card-title">{{post.title}}</h3>
                            <p class="card-subtitle">{{post.title}}</p>
                            <div class="card-meta">
                                <div class="meta-item">
                                    <svg class="meta-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                                    </svg>
                                    <span>{{post.date_created}}</span>
                                </div>
                                <div class="meta-item">
                                    <svg class="meta-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                                    </svg>
                                    <span>8 min</span>
                                </div>
                            </div>
                            <div class="read-more">
                                Read More
                                <svg class="arrow-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path>
                                </svg>
                            </div>
                        </div>
                    </a>
                </div>
    {% endfor %}
                """