from django import forms
from .models import Post, Comment, User
from django.contrib.auth.forms import AuthenticationForm


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "email", "password"]


class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content"]  # Поля, которые можно редактировать
        widgets = {
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
            "title": forms.TextInput(attrs={"class": "form-control"}),
        }


class UserLoginForm(AuthenticationForm):
    pass
