from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.conf import settings
from django.utils.text import slugify
from django.views.generic import ListView,  DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post
from .models import NewsletterSubscriber, Category
from .forms import CommentForm, PostForm

#this is where htmx will come in. once the comment is filled in and the user hits submit, the 
#comment form is replaced by the comment itself
def add_comment(request):
    if request.method == "POST":
        form = CommentForm(request.POST)

        if form.is_valid():
            #first send an email to the user containing the body of the message. 
            # if success, then save the comment
            comment = form.save()

            # Newsletter subscription
            if form.cleaned_data.get("subscribe"):
                email = form.cleaned_data["email"]
                name = form.cleaned_data["name"]

                if not NewsletterSubscriber.objects.filter(email=email).exists():
                    NewsletterSubscriber.objects.create(
                        email=email,
                        name=name
                    )

            return redirect("comment_success")

    else:
        form = CommentForm()

    return render(request, "blog/add_comment.html", {"form": form})


User = settings.AUTH_USER_MODEL

class PostListView(ListView):
    model  =  Post
    template_name = 'blog/post_list.html' #<app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-created_date']
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html' #<app>/<model>_<viewtype>.html
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = self.object.comments.all()

        related_posts = Post.objects.all()[:3]

        context['related_posts'] = related_posts
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            # no request.user here, we rely on form fields since no auth is required
            comment.full_name = form.cleaned_data['full_name']
            comment.email = form.cleaned_data['email']
            comment.content = form.cleaned_data['content']
            comment.save()

            #subscribe to newsletter check!
            if form.cleaned_data['subscribe']:
                NewsletterSubscriber.objects.get_or_create(email=form.cleaned_data['email'],
                                                    defaults={"full_name":form.cleaned_data['full_name']})
            

            return redirect('post-detail', slug=self.object.slug)
       
        return self.get(request, *args, **kwargs)


class UserPostListView(ListView):
    model  =  Post
    template_name = 'blog/user_posts.html' #<app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, email=self.kwargs.get('email'))
        return Post.objects.filter(author=user).order_by('-created_date')
    

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.slug = slugify(form.instance.title)
        return super().form_valid(form)
        
    def get_success_url(self):
        return reverse('post-detail', kwargs={'slug': self.object.slug})

        

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'excerpt', 'category', 'featured_image', 'is_featured']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
        
    

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    template_name = 'blog/post_confirm_delete.html'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
            


