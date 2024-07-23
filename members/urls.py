from django.contrib import admin
from django.urls import path
from . import views

urlpatterns =[
    path('loginuser/',views.login_user, name='login_user'),
    path('registeruser/',views.user_signup,name='register_user'),
    path('logout/', views.logout_user, name='logout_user'), 
]

