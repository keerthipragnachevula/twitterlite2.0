from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', views.register, name='register'),
    path('create/', views.create_post, name='create_post'),
    path('delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('user/<str:username>/', views.profile, name='profile'),
]