from rest_framework import serializers
from django.contrib.auth.models import User as UU
from api.models import *
import datetime

class UUSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = '__all__'
        fields = ('id', 'nickname')


class UserSerializer(serializers.ModelSerializer):
    place = serializers.CharField(required=False)
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = User
        fields = '__all__'
        
class PPSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        # fields = '__all__'
        fields = ['name']

class ProductPhotoSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(use_url=True)

    class Meta:
        model = ProductPhoto
        fields = ['photo']


class ProductSerializer(serializers.ModelSerializer):
    # user = UserSerializer(read_only=True)
    name = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    caution = serializers.CharField(required=False)
    price = serializers.CharField(required=False)
    price_prop = serializers.CharField(required=False)
    user = UserSerializer(read_only=True)
    photos = serializers.SerializerMethodField()

    def get_photos(self, obj):
        photo = obj.productphoto_set.all()
        return ProductPhotoSerializer(instance=photo, many=True, context=self.context).data

    class Meta:     
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        instance = Product.objects.create(**validated_data)
        photo_set = self.context['request'].FILES
        for photo_data in photo_set.getlist('photo'):
            ProductPhoto.objects.create(product=instance, photo=photo_data)
        return instance


class DealSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    user = UserSerializer(read_only=True)
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


class DealReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = DealReview
        fields = '__all__'


class ProductReviewSerializer(serializers.ModelSerializer):
    user = UUSerializer(read_only=True)
    product = PPSerializer(read_only=True)
    class Meta:
        model = ProductReview
        # fields = '__all__'
        fields = ('user', 'product', 'score', 'content', 'created_at')


class FavoriteSerializer(serializers.ModelSerializer):
    user = UUSerializer(read_only=True)
    class Meta:
        model = Favorite
        fields = ('user', 'product')
        # fields = '__all__'


class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = '__all__'