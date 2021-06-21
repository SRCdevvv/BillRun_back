from rest_framework_jwt.settings import api_settings
from rest_framework import fields, serializers
from django.contrib.auth.models import User as UU, update_last_login
from django.contrib.auth import authenticate, get_user_model, login
from .auth_backend import PasswordlessAuthBackend
from .models import *
import datetime

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


class UUSerializer(serializers.ModelSerializer): #간단쓰
    class Meta:
        model = BillrunUser
        # fields = '__all__'
        fields = ('id', 'nickname')

class UserSerializer(serializers.ModelSerializer):
    # place = serializers.CharField(required=False)
    # username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = BillrunUser
        # fields = '__all__'
        fields = ['id', 'nickname', 'email', 'community', 'lat', 'lng', 'location', 'money', 'score', 'profile', 'is_active']

class UserCreateSerializer(serializers.ModelSerializer): #회원가입
    def create(self, validated_data):
        user = BillrunUser.objects.create_user(
            phone = validated_data['phone'],
            community = validated_data['community'],
            email = validated_data['email'],
            # nickname = validated_data['nickname'],
            lat = validated_data['lat'],
            lng = validated_data['lng']
        )
        return user
    class Meta:
        model = BillrunUser
        # fields = '__all__'
        fields = ['phone', 'community', 'email', 'lat', 'lng', 'is_active']


class UserLoginSerializer(serializers.ModelSerializer): #로그인
    phone = serializers.CharField(max_length=11)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        phone = data.get("phone", None)
        user = PasswordlessAuthBackend.authenticate(phone=phone)
        print(user) #로그인유저확인!
        if user is None:
            return {
                'phone': 'None'
            }
        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)
        except BillrunUser.DoesNotExist:
            raise serializers.ValidationError(
                'User with given phone number does not exists'
            )
        return {
            'phone': user.phone,
            'token': jwt_token
        }

    class Meta:
        model = BillrunUser
        fields = ['phone', 'token']

class TermsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Terms
        fields = '__all__'

class PPSerializer(serializers.ModelSerializer): #간단
    class Meta:
        model = Product
        # fields = '__all__'
        fields = ['name']

class ProductPhotoSerializer(serializers.ModelSerializer): #물품사진불러올때
    photo = serializers.ImageField(use_url=True)

    class Meta:
        model = ProductPhoto
        fields = ['photo']

class ProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    photos = serializers.SerializerMethodField()
    description = serializers.CharField(required=False)
    caution = serializers.CharField(required=False)
    price = serializers.CharField(required=False)
    price_prop = serializers.CharField(required=False)
    user = UUSerializer(read_only=True)
    lat = serializers.IntegerField(required=False)
    lng = serializers.IntegerField(required=False)

    def get_photos(self, obj):
        photo = obj.productphoto_set.all()
        return ProductPhotoSerializer(instance=photo, many=True, context=self.context).data

    class Meta:     
        model = Product
        fields = '__all__'
        # fields = ['name', 'description', 'caution', 'user', 'price', 'price_prop', 'lat', 'lng', 'photos']

    def create(self, validated_data):
        instance = Product.objects.create(**validated_data)
        photo_set = self.context['request'].FILES
        for photo_data in photo_set.getlist('photo'):
            ProductPhoto.objects.create(product=instance, photo=photo_data)
        return instance

class ProductPostSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(use_url=True)
    # photos = serializers.ImageField(source='product.photos')

    # def create(self, validated_data):
    #     photos = validated_data.get("product", {}).get('photos')
    #     return photos

    def get_photos(self, obj):
        photo = obj.productphoto_set.all()
        return ProductPhotoSerializer(instance=photo, many=True).data

    def create(self, validated_data):
        instance = Product.objects.create(**validated_data)
        photo_set = self.context['request'].FILES
        for photo_data in photo_set.getlist('photo'):
            ProductPhoto.objects.create(product=instance, photo=photo_data)
        return instance
    
    class Meta:
        model = Product
        # fields = '__all__'
        fields = ['lend', 'name', 'photo', 'description', 'caution', 'user', 'price', 'price_prop']


class DealSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    datentime = serializers.DateTimeField(required=False)
    period = serializers.CharField(required=False)

    class Meta:
        model = Deal
        # fields = '__all__'
        fields = ('id', 'product_id', 'user', 'period', 'datentime', 'deal_prop', 'deal_option')

class DDSerializer(serializers.ModelSerializer):
    product = PPSerializer(read_only=True)
    class Meta:
        model = Deal
        fields = ['product']


# class ReviewSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Review
#         fields = '__all__'

class DealReviewSerializer(serializers.ModelSerializer):
    user = UUSerializer(read_only=True)
    class Meta:
        model = DealReview
        # fields = '__all__'
        # fields = ('q1', 'q2', 'q3', 'user', 'created_at')
        fields = ('q1', 'q2', 'q3', 'q4', 'user', 'created_at')

class ProductReviewSerializer(serializers.ModelSerializer):
    user = UUSerializer(read_only=True)
    deal = DDSerializer(read_only=True)
    class Meta:
        model = ProductReview
        # fields = '__all__'
        fields = ('deal', 'content', 'score', 'user', 'created_at')
        # fields = ('deal', 'content', 'score', 'created_at')


class FavoriteSerializer(serializers.ModelSerializer):
    # user = UUSerializer(read_only=True)
    class Meta:
        model = Favorite
        fields = ('user', 'product')
        # fields = '__all__'


class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = '__all__'