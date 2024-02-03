from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["email"]


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ["nickname", "profile", "profile_image", "region", "region_detail"]


class LoginForm(forms.Form):
    email = forms.CharField(
        max_length=100, required=True, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "이메일"})
    )
    password = forms.CharField(
        max_length=30, required=True, widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "패스워드"})
    )