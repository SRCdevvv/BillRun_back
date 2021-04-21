from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.utils import timezone
from random import randint

import sys
import os
import hashlib
import hmac
import base64
import requests
import time

import json
import urllib.request

profile_default = 'user/default_user.png'
photo_default = 'photo/no_image.png'

SERVICE_ID = 'ncp:sms:kr:266096135165:billrun'
ACCESS_KEY = '9MMMH1wL9iCCYZzSpOB2'
SECRET_KEY = '1Ym0fRLpuxOz7YD92w7ppy7YqLeT48pjPFdhLzwx' #계정 시크릿키

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
            'from': '01066278667',
            'content': '인증 번호 [{}]를 입력해주세요.'.format(self.auth_number),
            'messages':[{
                    'to':self.phone_number
                }]
        }
        requests.post(apiUrl, headers=headers, data=json.dumps(body))
    
    def test(self):
        print(self.phone_number)
        print(type(self.make_signature()))


# User
class User(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=10, default='', unique=True)
    money = models.IntegerField(default=0)
    level = models.CharField(max_length=10, default='', null=True, blank=True)
    place = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add = True, null= True)
    updated_at = models.DateTimeField(auto_now = True, null= True)
    
    def upload_profile(self, filename):
        path = 'user/{}'.format(filename)
        return path

    profile = models.ImageField(upload_to=upload_profile, null=True, blank=True, default=profile_default)

    def __str__(self):
        return f"{self.id}) {self.nickname}({self.user.username})"


class Product(models.Model):
    DEFAULT_PK=1
    PRICEPROP = (
        ('Day', 'Per Day'),
        ('30m', 'Per half hour'),
        ('1h', 'Per hour'),
    )
    # DEALOP = (
    #     ('F2F', 'Face to Face'),
    #     ('Untact', 'Untact'),
    # )

    category = models.BooleanField(default=True) 
    name = models.CharField(max_length=50)
    description = models.TextField()
    caution = models.TextField()
    price = models.IntegerField()
    price_prop = models.CharField(max_length=10, choices=PRICEPROP)
    place_option = models.BooleanField(default=True)
    hits = models.IntegerField(default=0)
    like_count = models.PositiveIntegerField(default=0)
    # deal_option = models.CharField(max_length=10, null=True, blank=True, default="", choices=DEALOP)
    user_id = models.ForeignKey(User, default=DEFAULT_PK, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True, null= True)
    updated_at = models.DateTimeField(auto_now = True, null= True)

    def upload_photo(self, filename):
        path = 'photo/{}'.format(filename)
        return path

    photo = models.ImageField(upload_to=upload_photo, null=True, blank=True, default=photo_default)

    def __str__(self):
        if self.category:
            return f"{self.id}) [빌려드림]{self.name} - {self.user_id.nickname}"
        else:
            return f"{self.id}) [빌림]{self.name} - {self.user_id.nickname}"


class Deal(models.Model):
    DEFAULT_PK=1
    DEALPROP = (
        ('Not', 'Not Yet'),
        ('PRO', 'In Progress'),
        ('COM', 'Complete'),
    )
    # DEALOP = (
    #     ('F2F', 'Face to Face'),
    #     ('Untact', 'Untact'),
    # )
    deal_prop = models.CharField(max_length=10, choices=DEALPROP)
    contract = models.BooleanField(default=False)
    contract2 = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    datentime = models.DateTimeField(auto_now=False, blank=False, null=False)
    period = models.IntegerField()
    # deal_option = models.CharField(max_length=10, default="", choices=DEALOP)
    user_id = models.ForeignKey(User, default=DEFAULT_PK, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, default=DEFAULT_PK, on_delete=models.CASCADE)

    def __str__(self):
        if self.product_id.category:
            return f"{self.id}) [빌려드림]{self.product_id.name} ({self.product_id.user_id.nickname} >> {self.user_id.nickname})"
        else:
            return f"{self.id}) [빌림]{self.product_id.name} ({self.product_id.user_id.nickname} >> {self.user_id.nickname})"


class Review(models.Model):
    DEFAULT_PK=1
    post = models.TextField()
    product_score = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    user_score = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    deal_id = models.ForeignKey(Deal, default=DEFAULT_PK, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, default=DEFAULT_PK, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, default=DEFAULT_PK, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True, null= True)
    updated_at = models.DateTimeField(auto_now = True, null= True)

    def __str__(self):
        return f"{self.deal_id.id}) {self.product_id.name} - {self.user_id.nickname}"

    def upload_review(self, filename):
        path = 'review/{}'.format(filename)
        return path

    photo = models.ImageField(upload_to=upload_review, null=True, blank=True)


class Favorite(models.Model):
    DEFAULT_PK=1
    user = models.ForeignKey(User, default=DEFAULT_PK, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product, blank=True)
    created_at = models.DateTimeField(auto_now_add = True, null= True)
    updated_at = models.DateTimeField(auto_now = True, null= True)

    def __str__(self):
        return f"{self.user.nickname}의 찜 목록"

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