from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('signup/',views.signup, name = "signup"),
    path('login/',views.user_login, name = "login"),
    path('logout/',views.user_logout, name = "logout"),
    path('password/',views.user_password, name = "user_password"),
    path('user-id/',views.user_id, name = "user_id"),
    path('logincheck/',views.loginCheck, name = 'logincheck'),
    path('new-password/', views.new_password, name = 'new_password'),
    path('loginValidate/',views.loginValidate, name = 'loginValidate')
]
