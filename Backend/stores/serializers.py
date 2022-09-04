from rest_framework import serializers
from .models import Stores, Images


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stores
        fields = ('id', 'store_name', 'main_menu',
                  'longitude', 'latitude', 'user')


class StoreRandomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stores


class Stores_Information(serializers.ModelSerializer):
    class Meta:
        model = Stores
        fields = "__all__"


class Serializers_Images(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ('image1', 'image2', 'image3')
