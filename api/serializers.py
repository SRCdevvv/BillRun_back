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


# class ProductPhotoSerializer(serializers.ModelSerializer): #물품사진불러올때
#     photo = serializers.ImageField(use_url=True)

#     class Meta:
#         model = ProductPhoto
#         fields = ['photo']


class ProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    caution = serializers.CharField(required=False)
    price = serializers.CharField(required=False)
    price_prop = serializers.CharField(required=False)
    user = UUSerializer(read_only=True)
    lat = serializers.IntegerField(required=False)
    lng = serializers.IntegerField(required=False)
    photo1 = serializers.ImageField(required=False)
    photo2 = serializers.ImageField(required=False)
    photo3 = serializers.ImageField(required=False)
    photo4 = serializers.ImageField(required=False)
    photo5 = serializers.ImageField(required=False)
    # count = serializers.SerializerMethodField(source='count_favortie')

    # def get_photos(self, obj):
    #     photo = obj.productphoto_set.all()
    #     return ProductPhotoSerializer(instance=photo, many=True, context=self.context).data

    class Meta:     
        model = Product
        fields = '__all__'
        # fields = ['name', 'description', 'caution', 'user', 'price', 'price_prop', 'lat', 'lng', 'photos']
    
    # def get_count(self):
    #     count = Favorite.objects.all().aggregate(Count('id'))
    #     return count

    # def create(self, validated_data):
    #     instance = Product.objects.create(**validated_data)
    #     photo_set = self.context['request'].FILES
    #     for photo_data in photo_set.getlist('photo'):
    #         ProductPhoto.objects.create(product=instance, photo=photo_data)
    #     return instance


class ProductPostSerializer(serializers.ModelSerializer):
    # photo = serializers.ImageField(use_url=True, required=False)
    # photo = serializers.ImageField(source='productphoto.photo')
    # photos = ProductPhotoSerializer(required=False) #원래이걸로해써횹
    # photo2 = ProductPhotoSerializer()
    # photo = serializers.SerializerMethodField()
    # photo2 = serializers.ImageField(use_url=True)
    # photos = serializers.ImageField()

    # def create(self, validated_data):
    #     photos = validated_data.get("photos", {}).get('photo') #'InMemoryUploadedFile' object has no attribute 'get'
    #     # photos = validated_data.get("p", {}).get('photo') #`create()` did not return an object instance.
    #     return photos

    # def get_photos(self, obj):
    #     photo = obj.productphoto_set.all()
    #     return ProductPhotoSerializer(instance=photo, many=True).data

    class Meta:
        model = Product
        # fields = '__all__'
        fields = ['lend', 'name', 'category', 'description', 'caution', 'user', 'price', 'price_prop', 'photo1', 'photo2', 'photo3', 'photo4', 'photo5']
        # 다 되고나서 위도경도도 추가할것!

    # def create(self, validated_data): #스오플보고 따라하는중
    #     photos_data = validated_data.pop('photos')
    #     product = super().create(**validated_data)
    #     for photo in photos_data:
    #         photo['product'] = product
    #         ProductPhoto.objects.create(**photo)
    #     # ProductPhoto.objects.create(product=product, **photo_data)
    #     return product

    # def create(self, validated_data): #될뻔한줄알았는데 테스트가 안됨
    #     photos_data = validated_data.pop('photos')
    #     product = Product.objects.create(**validated_data)
    #     for photo in photos_data:
    #         ProductPhoto.objects.create(product=product, **photos_data)
    #     # ProductPhoto.objects.create(product=product, **photo_data)
    #     return product

    # def create(self, validated_data): #원래이걸로해써횹
    #     photo_data = validated_data.pop('photo')
    #     product = Product.objects.create(**validated_data)
    #     # for photo in photo_data:
    #     #     product.photo.create(**photo)
    #     ProductPhoto.objects.create(product=product, **photo_data)
    #     return product

    # #Product() got an unexpected keyword argument 'photo'
    # def create(self, validated_data):
    #     instance = Product.objects.create(**validated_data)
    #     photo_set = self.context['request'].FILES
    #     for photo_data in photo_set.getlist('photo'):
    #         ProductPhoto.objects.create(product=instance, photo=photo_data)
    #     return instance
    

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