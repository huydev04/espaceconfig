from django.urls import path
from . import views

app_name="admin"

urlpatterns = [
    path('homeadmin/', views.home, name = 'home'),
    path('loginadmin', views.login, name='loginadmin'),
    path('logoutadmin/', views.Logout, name='logoutadmin'),
    path('censorship', views.censorship, name='censorship'),
]
