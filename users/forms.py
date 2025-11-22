
from django import forms
from .models import User, Profile
from django.contrib.auth.forms import (
    UserCreationForm
)

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "phone_number")

    def save(self, commit=True):
        user = super().save(commit)
        return user
    
    #profile is created in signals.py

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "phone_number", "email")

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user']
