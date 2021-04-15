from rest_framework import serializers
from django.contrib.auth.models import User as UU
from api.models import *
import datetime

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
        fields = '__all__'
        

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

class DealSerializer(serializers.ModelSerializer):
    product_id = ProductSerializer(read_only=True)
    user_id = UserSerializer(read_only=True)
    datentime = serializers.DateTimeField(required=False)
    period = serializers.CharField(required=False)
    class Meta:
        model = Deal
        fields = '__all__'
        # fields = ('id', 'product_id', 'user_id', 'period', 'datentime', 'deal_prop', 'deal_option')

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'