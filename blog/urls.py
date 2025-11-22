from django.urls import path
from .views import (PostListView, PostDetailView, 
                    PostCreateView, PostUpdateView, 
                    PostDeleteView, UserPostListView)

urlpatterns = [
    path('', PostListView.as_view(), name = 'blog-home'),
    path('user/<str:username>', UserPostListView.as_view(), name = 'user-posts'),
    path('new/', PostCreateView.as_view(), name = 'post-create'),
    path('<slug:slug>/', PostDetailView.as_view(), name = 'post-detail'), #order matters. never put this above /new
    path('<slug:slug>/update/', PostUpdateView.as_view(), name = 'post-update'),
    path('<slug:slug>/delete/', PostDeleteView.as_view(), name = 'post-delete'),
]