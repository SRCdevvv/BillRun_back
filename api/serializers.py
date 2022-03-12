from rest_framework_jwt.settings import api_settings
from rest_framework import fields, serializers
from django.contrib.auth.models import User as UU, update_last_login
from django.contrib.auth import authenticate, get_user_model, login
from .auth_backend import PasswordlessAuthBackend
from .models import *
import datetime

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

def serialize_chat(chat):
    return {
        "user":chat.user.pk,
        "room":chat.room.pk,
        "message":chat.message,
        "created_at":chat.created_at
    }

def serialize_chats(chats):
    return [serialize_chat(chat) for chat in chats]

def serialize_room(room):
    return {
        "from_user":room.from_user.pk,
        "from_user_name":room.from_user.nickname,
        "from_user_photo":room.from_user.profile,
        "to_user":room.to_user.pk,
        "to_user_name":room.to_user.nickname,
        "to_user_photo":room.to_user.profile,
        "chats":serialize_chats(room.to_chats)
    }

def serializer_rooms(rooms):
    return [serialize_room(room) for room in rooms]


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
    token = serializers.SerializerMethodField()

    def get_token(self, data):
        user = data.user
        if user is None:
            return {
                'user is None'
            }
        payload = JWT_PAYLOAD_HANDLER(user)
        jwt_token = JWT_ENCODE_HANDLER(payload)
        return jwt_token

    class Meta:
        model = Terms
        # fields = '__all__'
        fields = ['user', 'token', 'service', 'privacy', 'location', 'marketing']


class PPSerializer(serializers.ModelSerializer): #간단
    class Meta:
        model = Product
        # fields = '__all__'
        fields = ['id', 'name']


class ProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    caution = serializers.CharField(required=False)
    price = serializers.CharField(required=False)
    price_prop = serializers.CharField(required=False)
    user = UUSerializer(read_only=True)
    lat = serializers.FloatField(required=False)
    lng = serializers.FloatField(required=False)

    class Meta:     
        model = Product
        fields = '__all__'
        # fields = ['name', 'description', 'caution', 'user', 'price', 'price_prop', 'lat', 'lng', 'photos']


class ProductPostSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        obj = Product.objects.create(**validated_data)
        if '/o/' in obj.photo1:
            url_list = obj.photo1.split('/o/')
            obj.photo1 = url_list[1]
        if '/o/' in obj.photo2:
            url_list = obj.photo2.split('/o/')
            obj.photo2 = url_list[1]
        if '/o/' in obj.photo3:
            url_list = obj.photo3.split('/o/')
            obj.photo3 = url_list[1]
        if '/o/' in obj.photo4:
            url_list = obj.photo4.split('/o/')
            obj.photo4 = url_list[1]
        if '/o/' in obj.photo5:
            url_list = obj.photo5.split('/o/')
            obj.photo5 = url_list[1]
        obj.save()
        return obj
   
    class Meta:
        model = Product
        # fields = '__all__'
        fields = ['lend', 'name', 'category', 'description', 'caution', 'user', 'price', 'price_prop', 'photo1', 'photo2', 'photo3', 'photo4', 'photo5']
        # 다 되고나서 위도경도도 추가할것!


class DealSerializer(serializers.ModelSerializer):
    product = PPSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    datentime = serializers.DateTimeField(required=False)
    period = serializers.CharField(required=False)

    class Meta:
        model = Deal
        # fields = '__all__'
        fields = ('id', 'product', 'user', 'period', 'datentime', 'deal_prop')


class DDSerializer(serializers.ModelSerializer):
    product = PPSerializer(read_only=True)
    class Meta:
        model = Deal
        fields = ['product']


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