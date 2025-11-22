from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from blog.models import Post
from portfolio.models import PortfolioItem


def home(request):
    posts = Post.objects.all()[:3]
    recent_works = PortfolioItem.objects.all()[:3]
    context = {'posts': posts,
                'recent_works': recent_works}
    return render(request, 'core/home.html', context )

def about(request):
    return render(request, 'core/about.html')

def main(request):
    return render(request, 'core/base.html')
#just for rendering base.html. helpful for styling it