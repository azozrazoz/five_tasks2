from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from .forms import PostEditForm, PostForm, CommentForm, UserLoginForm, UserRegisterForm
from .models import Post
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login


def home(request):
    posts = Post.objects.filter(is_active=True).order_by("-created_at")
    paginator = Paginator(posts, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "home.html", {"page_obj": page_obj})


def post_list(request):
    posts = Post.objects.all()
    return render(request, "main/post_list.html", {"posts": posts})


def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("post_list")
    else:
        form = PostForm()
    return render(request, "main/create_post.html", {"form": form})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()

    if request.method == "POST":
        form = PostEditForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect("post_detail", pk=post.pk)
    else:
        form = PostEditForm(instance=post)

    is_author = post.author == request.user

    return render(
        request,
        "main/post_detail.html",
        {
            "post": post,
            "comments": comments,
            "form": form,
            "is_author": is_author,
        },
    )


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if post.author != request.user:
        return redirect("post_detail", pk=post.pk)

    if request.method == "POST":
        form = PostEditForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect("post_detail", pk=post.pk)
    else:
        form = PostEditForm(instance=post)

    return render(request, "main/post_edit.html", {"form": form, "post": post})


def create_comment(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect("post_detail", pk=pk)
    else:
        form = CommentForm()
    return render(request, "main/create_comment.html", {"form": form, "post": post})


class UserView(APIView, PageNumberPagination):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            user = get_object_or_404(User, pk=pk, is_active=True)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        else:
            users = User.objects.filter(is_active=True)
            results = self.paginate_queryset(users, request, view=self)
            serializer = UserSerializer(results, many=True)
            return self.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
def get_jwt_token(request):
    user = request.user
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    return Response({"access": access_token, "refresh": str(refresh)})


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = UserRegisterForm()

    return render(request, "register.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # refresh = RefreshToken.for_user(user)

                # response = JsonResponse({'message': 'Login successful.'})
                # response.set_cookie(
                #     key='access_token',
                #     value=str(refresh.access_token),
                #     httponly=True,
                #     secure=True,  # Используйте True в продакшене
                #     samesite='Lax',
                # )
                # response.set_cookie(
                #     key='refresh_token',
                #     value=str(refresh),
                #     httponly=True,
                #     secure=True,  # Используйте True в продакшене
                #     samesite='Lax',
                # )
                
                return redirect("home")
            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = UserLoginForm()

    return render(request, "login.html", {"form": form})
