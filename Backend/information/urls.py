from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('editors/', views.get_editors, name = "editors")
]
