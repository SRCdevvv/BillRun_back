from rest_framework import serializers
from django.contrib.auth.models import User as UU
from api.models import *

class UUSerializer(serializers.ModelSerializer):
    class Meta:
        model = UU
        fields = '__all__'
        # fields = ('username')

class UserSerializer(serializers.ModelSerializer):
    username = UUSerializer(read_only=True)
    class Meta:
        model = User
        fields = ('id', 'place', 'username')
        # fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'