"""
URL configuration for exam project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from main import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('', views.home, name='home'),
    path("admin/", admin.site.urls),
    path("post/new/", views.create_post, name="create_post"),
    path("post/<int:pk>/comment/", views.create_comment, name="create_comment"),
    path('posts/', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('api/users/', views.UserView.as_view(), name='user_list'),
    path('api/users/<int:pk>/', views.UserView.as_view(), name='user_detail'),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'), 
    path('api/token/admin/', views.get_jwt_token, name='admin_token'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
]
