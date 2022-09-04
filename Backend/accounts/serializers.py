from rest_framework import serializers
from .models import Users


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('user_id', 'nickname', 'user_num', 'emoji', 'user_information', 'identification', 'password')