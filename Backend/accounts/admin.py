from .models import Users
from atexit import register
from django.contrib import admin


admin.site.register(Users)
