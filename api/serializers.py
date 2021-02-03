from rest_framework import serializers
from django.contrib.auth.models import User as UU
from api.models import *

class UUSerializer(serializers.ModelSerializer):
    class Meta:
        model = UU
        fields = '__all__'
        # fields = ('username')

class UserSerializer(serializers.ModelSerializer):
    place = serializers.CharField(required=False)
    username = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = User
        fields = ('id', 'username', 'place')
        # fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    # user = UserSerializer(read_only=True)
    name = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    caution = serializers.CharField(required=False)
    price = serializers.CharField(required=False)
    price_prop = serializers.CharField(required=False)
    user_id = UserSerializer(read_only=True)
    class Meta:     
        model = Product
        fields = '__all__'