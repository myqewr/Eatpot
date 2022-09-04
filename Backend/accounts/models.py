
from django.db import models

# Create your models here.
from django.contrib.auth.models import User, AbstractUser

# 사용자


class Users(AbstractUser):
    phone_number = models.CharField(max_length=12, null=False, unique=True)
    role = models.BooleanField(null=True)  # 역할
    nickname = models.CharField(max_length=30, null=True, blank=True)  # 닉네임
    user_num = models.IntegerField(blank=True, null=True)  # 인덱스 순서
    emoji = models.ImageField(null=True, blank=True)  # 이모지
    user_information = models.CharField(
        max_length=100, null=True, blank=True)  # 한줄 소개
    refresh_token = models.TextField(null=True, blank=True)  # refresh token
