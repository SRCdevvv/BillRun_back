from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from cryptography.fernet import Fernet
from random import randint
from .secret import *
# from urllib.parse import unquote

import hashlib
import hmac
import base64
import requests
import time
import json

profile_default = 'user/default_user.png'
photo_default = 'photo/no_image.png'

# Auth
class AuthSms(models.Model):
    phone_number = models.CharField(verbose_name='휴대폰 번호', primary_key=True, max_length=11)
    auth_number = models.IntegerField(verbose_name='인증 번호')

    class Meta:
        db_table = 'auth_numbers'

    def save(self, *args, **kwargs):
        self.auth_number = randint(1000, 10000)
        super().save(*args, **kwargs)
        self.send_sms() # 인증번호가 담긴 SMS를 전송
        print("전송 완료")

    def send_sms(self):
        timestamp = str(int(time.time() * 1000))
        secret_key = bytes(SECRET_KEY, 'UTF-8')
        url = "https://sens.apigw.ntruss.com"
        requestUrl = "/sms/v2/services/"
        requestUrl2 = "/messages"
        uri = requestUrl + SERVICE_ID + requestUrl2
        apiUrl = url+ uri
        serviceId = SERVICE_ID
        access_key = ACCESS_KEY
        method = "POST"
        message = method + " " + uri + "\n" + timestamp + "\n" + access_key
        message = bytes(message, 'UTF-8')
        signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'x-ncp-apigw-timestamp': timestamp,
            'x-ncp-iam-access-key': access_key,
            'x-ncp-apigw-signature-v2': signingKey,
        }
        body = {
            'type': 'SMS',
            'from': PHONE,
            'content': '인증 번호 [{}]를 입력해주세요.'.format(self.auth_number),
            'messages':[{
                    'to':self.phone_number
                }]
        }
        requests.post(apiUrl, headers=headers, data=json.dumps(body))



# class User(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     nickname = models.CharField(max_length=10, default='', unique=True)
#     phone = models.CharField(max_length=11, blank=True)
#     money = models.IntegerField(default=0)
#     # level = models.CharField(max_length=10, default='', null=True, blank=True)
#     score = models.IntegerField(default=10)
#     place = models.CharField(max_length=50)
#     created_at = models.DateTimeField(auto_now_add = True, null= True)
#     updated_at = models.DateTimeField(auto_now = True, null= True)
    
#     def upload_profile(self, filename):
#         path = 'user/{}'.format(filename)
#         # unquote(path)
#         return path

#     profile = models.ImageField(upload_to=upload_profile, null=True, blank=True, default=profile_default)

#     def __str__(self):
#         return f"{self.id}) {self.nickname}({self.user.username})"


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, phone, community, email, nickname, lat, lng):
        if not phone:
            raise ValueError('핸드폰 번호를 입력해주세요.')
        #TODO raise 오류 여러개 추가
        n = randint(1000,9999)
        # nick = "빌런" + n
        fernet = Fernet(ENCODE_KEY)
        #TODO 닉네임 랜덤생성으로 바꿀것
        #TODO 중복체크추가할것
        user = self.model(
            # phone = fernet.encrypt(phone.encode()),
            phone = phone,
            community = community,
            email = self.normalize_email(email),
            nickname = nickname + str(n),
            lat = lat,
            lng = lng
        )
        # user.set_password(password)
        user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, email, nickname):
        #TODO 관리자 수만큼 숫자따와서 이름 옆에 붙여주기. 닉네임은 굳이 생성할 필요가 없어서
        fernet = Fernet(ENCODE_KEY)
        user = self.create_user(
            # phone = fernet.encrypt(bytes(phone, 'utf-8')),
            phone = phone,
            community = 1,
            email = email,
            nickname = nickname,
            lat = 0, 
            lng = 0,
            # password = password
        )
        user.is_active = True
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class BillrunUser(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()
    Group = (
        ('한양대', '한양대학교'),
        # ('가천대', '가천대학교'),
        # ('동국대', '동국대학교'),
        ('관리자', '기타'),
    )

    phone = models.CharField(max_length=11, unique=True)
    community = models.CharField(max_length=30, choices=Group)
    email = models.EmailField(max_length=254, unique=True)
    nickname = models.CharField(max_length=20, unique=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6) #위도
    lng = models.DecimalField(max_digits=9, decimal_places=6) #경도

    money = models.IntegerField(default=0)
    score = models.IntegerField(default=10)
    
    def upload_profile(self, filename):
        path = 'user/{}'.format(filename)
        # unquote(path)
        return path

    profile = models.ImageField(upload_to=upload_profile, null=True, blank=True, default=profile_default)

    def __str__(self):
        return f"{self.id}) {self.nickname}"
    
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    is_active = models.BooleanField(default=True)    #TODO
    is_admin = models.BooleanField(default=False)    
    is_superuser = models.BooleanField(default=False)    
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['nickname', 'email']


class Product(models.Model):
    DEFAULT_PK=1
    PRICEPROP = (
        ('Day', '일 당'),
        ('30m', '30분 당'),
        ('1h', '시간 당'),
    )
    GROUP = (
        ('Woman', '여성의류/잡화'),
        ('Man', '남성의류/잡화'),
        ('Digital', '디지털/가전'),
        ('MajorBook', '전공도서'),
        ('MajorEtc', '전공기타'),
        ('Game', '게임'),
        ('Sports', '스포츠'),
        ('Household', '생활잡화'),
        ('Etc', '기타'),
    )

    lend = models.BooleanField(default=True)
    category = models.CharField(max_length=10, choices=GROUP)
    name = models.CharField(max_length=50)
    description = models.TextField()
    caution = models.TextField()
    price = models.IntegerField()
    price_prop = models.CharField(max_length=10, choices=PRICEPROP)
    place_option = models.BooleanField(default=True) #안심거래옵션
    hits = models.IntegerField(default=0)
    like_count = models.PositiveIntegerField(default=0)
    # user = models.ForeignKey(User, default=DEFAULT_PK, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True, null= True)
    updated_at = models.DateTimeField(auto_now = True, null= True)

    # def __str__(self):
    #     if self.lend:
    #         return f"{self.id}) [빌려드림]{self.name} - {self.user.nickname}"
    #     else:
    #         return f"{self.id}) [빌림]{self.name} - {self.user.nickname}"
    def __str__(self):
        if self.lend:
            return f"{self.id}) [빌려드림]{self.name}"
        else:
            return f"{self.id}) [빌림]{self.name}"


class ProductPhoto(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    def upload_photo(self, filename):
        path = 'photo/{}'.format(filename)
        return path

    photo = models.ImageField(upload_to=upload_photo, null=True, blank=True, default=photo_default)

    def __str__(self):
        return f"{self.product}"
    

class Deal(models.Model):
    DEFAULT_PK=1
    DEALPROP = (
        ('NOT', 'Not Yet'),
        ('PRO', 'In Progress'),
        ('COM', 'Complete'),
    )

    deal_prop = models.CharField(max_length=10, default=1, choices=DEALPROP)
    contract = models.BooleanField(default=False)
    contract2 = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    datentime = models.DateTimeField(auto_now=False, blank=False, null=False)
    period = models.IntegerField()
    # user = models.ForeignKey(User, default=DEFAULT_PK, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, default=DEFAULT_PK, on_delete=models.CASCADE)

    # def __str__(self):
    #     if self.product.lend:
    #         return f"{self.id}) [빌려드림]{self.product.name} ({self.product.user.nickname} >> {self.user.nickname})"
    #     else:
    #         return f"{self.id}) [빌림]{self.product.name} ({self.product.user.nickname} >> {self.user.nickname})"
    def __str__(self):
        if self.product.lend:
            return f"{self.id}) [빌려드림]{self.product.name}"
        else:
            return f"{self.id}) [빌림]{self.product.name}"

#Review
class Review(models.Model):
    DEFAULT_PK=1
    post = models.TextField()
    product_score = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    user_score = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    deal = models.ForeignKey(Deal, default=DEFAULT_PK, on_delete=models.CASCADE)
    # user = models.ForeignKey(User, default=DEFAULT_PK, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, default=DEFAULT_PK, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True, null= True)
    updated_at = models.DateTimeField(auto_now = True, null= True)

    def __str__(self):
        return f"{self.deal.id}) {self.product.name} - {self.user.nickname}"

    def upload_review(self, filename):
        path = 'review/{}'.format(filename)
        return path

    photo = models.ImageField(upload_to=upload_review, null=True, blank=True)

class DealReview(models.Model):
    DEFAULT_PK=1
    SCOREPROP = (
        ('상', '상'),
        ('중', '중'),
        ('하', '하'),
    )
    q1 = models.CharField(max_length=30, default=1, choices=SCOREPROP)
    q2 = models.CharField(max_length=30, default=1, choices=SCOREPROP)
    q3 = models.CharField(max_length=30, default=1, choices=SCOREPROP)
    deal = models.ForeignKey(Deal, default=DEFAULT_PK, on_delete=models.CASCADE)
    # user = models.ForeignKey(User, default=DEFAULT_PK, on_delete=models.CASCADE) #리뷰작성자
    created_at = models.DateTimeField(auto_now_add = True, null= True)
    updated_at = models.DateTimeField(auto_now = True, null= True)

    # def __str__(self):
    #     return f"{self.user.nickname} - {self.deal}"
    def __str__(self):
        return f"{self.deal}"

class ProductReview(models.Model):
    DEFAULT_PK=3
    score = models.FloatField(validators=[MinValueValidator(0.5), MaxValueValidator(5)])
    content = models.TextField()
    deal = models.ForeignKey(Deal, default=DEFAULT_PK, on_delete=models.CASCADE)
    # user = models.ForeignKey(User, default=DEFAULT_PK, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True, null= True)
    updated_at = models.DateTimeField(auto_now = True, null= True)

    # def __str__(self):
    #     return f"{self.user.nickname} - {self.deal.product.name}"
    def __str__(self):
        return f"{self.deal.product.name}"

class Favorite(models.Model):
    DEFAULT_PK=1
    # user = models.ForeignKey(User, default=DEFAULT_PK, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product, blank=True)
    created_at = models.DateTimeField(auto_now_add = True, null= True)
    updated_at = models.DateTimeField(auto_now = True, null= True)

    # def __str__(self):
    #     return f"{self.user.nickname}의 찜 목록"

class Notice(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True, null= True)
    updated_at = models.DateTimeField(auto_now = True, null= True)
    
    def upload_banner(self, filename):
        path = 'notice/banner/{}'.format(filename)
        return path

    def upload_contentphoto(self, filename):
        path = 'notice/content/{}'.format(filename)
        return path

    def __str__(self):
        return f"{self.id}) {self.title}"
    banner_photo = models.ImageField(upload_to=upload_banner)
    content_photo = models.ImageField(upload_to=upload_contentphoto, null=True, blank=True)