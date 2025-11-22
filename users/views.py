from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages #message methods  .debug .info .success .error
from django.contrib.auth import logout
from .models import Profile
from blog.models import Post
User = get_user_model()

 
def logout_view(request):
    logout(request)
    return redirect('home')

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # Profile created automatically in signals.py
            messages.success(request, "Your account has been created! You can now log in.")
            return redirect("login")
    else:
        form = UserRegisterForm()

    return render(request, "users/register.html", {"form": form})


@login_required
def profile(request):
    #django.contrib.auth.context_processors.auth already handles everything
    #but a fallback in case everything doesn't go to plan
    profile = Profile.objects.get_or_create(user=request.user)
    posts = Post.objects.filter(author=request.user)
    context = {'profile': profile, 'posts': posts}
    return render(request, "users/profile.html", context)


@login_required
def update_user(request):
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your account has been updated successfully!")
            return redirect("profile")  # Replace with your profile view name
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
    }
    return render(request, "users/update_user.html", context)
