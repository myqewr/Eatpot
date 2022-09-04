from rest_framework import serializers
from accounts.models import Users


class InformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        # 인덱스 순서, 닉네임, 이모지, 한 줄 소개
        fields = ('user_num', 'nickname', 'emoji', 'user_information')