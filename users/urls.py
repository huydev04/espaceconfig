from django.urls import path
from . import views

app_name="user"

urlpatterns = [
    path('', views.home, name = 'home'),
    path('profile/', views.profile, name = 'profile'),
    path('login/', views.login, name = 'login'),
    path('register/', views.register, name = 'register'),
    path('logout/', views.Logout, name = 'logout'),
    path('post/', views.Post, name = 'post'),
    path('posted/', views.Posted, name = 'posted'),
    path('reader/', views.readpage, name = 'reader'),
    path('account/', views.account, name = 'account'),
]
