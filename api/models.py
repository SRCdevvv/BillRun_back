import uuid
from uuid import uuid4
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db.models.fields.related import ForeignKey
from django.utils import timezone
from cryptography.fernet import Fernet
from random import randint
from django.db.models import Count
# from BillRun_back.my_settings import *

from urllib.parse import quote
import hashlib
import hmac
import base64
import requests
import time
import json
import os

profile_default = 'default/default_user.png'
photo_default = 'default/no_image.png'

#SMS
PHONE = '01066278667'
NAVER_ACCESS_KEY = '9MMMH1wL9iCCYZzSpOB2'
NAVER_SECRET_KEY = '1Ym0fRLpuxOz7YD92w7ppy7YqLeT48pjPFdhLzwx'
SMS_SECRET_KEY = '2d99e064782c4640b5816ee9d762e792'
SMS_SERVICE_ID = 'ncp:sms:kr:266096135165:billrun'

# fernet = Fernet(ENCODE_KEY)

### Auth
class AuthSms(models.Model):
    phone = models.CharField(verbose_name='휴대폰 번호', max_length=110, unique=True)
    auth_number = models.IntegerField(verbose_name='인증 번호')

    # class Meta:
    #     db_table = 'auth_numbers'

    def save(self, *args, **kwargs):
        self.auth_number = randint(1000, 10000)
        super().save(*args, **kwargs)
        self.send_sms() # 인증번호가 담긴 SMS를 전송
        
    def send_sms(self):
        # phone = self.phone
        # phone_decrypted = fernet.decrypt(phone)

        timestamp = str(int(time.time() * 1000)) #시간제한 5분
        secret_key = bytes(NAVER_SECRET_KEY, 'UTF-8')
        url = "https://sens.apigw.ntruss.com"
        requestUrl = "/sms/v2/services/"
        requestUrl2 = "/messages"
        uri = requestUrl + SMS_SERVICE_ID + requestUrl2
        apiUrl = url+ uri
        serviceId = SMS_SERVICE_ID
        access_key = NAVER_ACCESS_KEY
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
            'content': '[빌RUN] 인증 번호 [{}]를 입력해주세요.'.format(self.auth_number),
            'messages':[{
                    'to':self.phone
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


### User
class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, phone, community, email, lat, lng):
        if not phone:
            raise ValueError('핸드폰 번호를 입력해주세요.')
        while True:
            n = randint(1000,9999)
            nickname = "빌런" + str(n)
            try: # 닉네임 중복체크
                BillrunUser.objects.get(nickname=nickname)
            except: # BillrunUser.DoesNotExist
                break
        # fernet = Fernet(ENCODE_KEY)
        #TODO 핸드폰번호 암호화
        user = self.model(
            # phone = fernet.encrypt(phone.encode()),
            phone = phone,
            community = community,
            email = self.normalize_email(email),
            nickname = nickname,
            lat = lat,
            lng = lng
        )
        user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, email, nickname, password):
        # fernet = Fernet(ENCODE_KEY)
        user = self.create_user(
            # phone = fernet.encrypt(bytes(phone, 'utf-8')),
            phone = phone,
            community = 1,
            email = email,
            lat = 0, 
            lng = 0,
        )
        user.nickname = nickname
        user.set_password(password)
        user.is_active = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class BillrunUser(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()
    Group = (
        ('한양대', '한양대학교'),
        # ('가천대', '가천대학교'),
        # ('동국대', '동국대학교'),
        ('관리자', '관리자'),
    )

    phone = models.CharField(max_length=110, unique=True)
    community = models.CharField(max_length=30, choices=Group)
    email = models.EmailField(max_length=254, unique=True)
    nickname = models.CharField(max_length=20, unique=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, default=37.55723) #위도
    lng = models.DecimalField(max_digits=9, decimal_places=6, default=127.04539) #경도
    location = models.CharField(max_length=50, default='', null=True, blank=True)

    money = models.IntegerField(default=0)
    score = models.IntegerField(default=10)
    
    def upload_profile(self, filename):
        ymd_path = timezone.now().strftime('%Y/%m/')
        uuid_name = uuid4().hex
        extension = os.path.splitext(filename)[-1].lower()
        path = f'{ymd_path}/user/{uuid_name + extension}'
        return path

    # profile = models.ImageField(upload_to=upload_profile, default=profile_default)
    profile = models.CharField(max_length=200, default="default%2Fdefault_user.png?alt=media&token=08fe3895-fdce-40f9-9176-a62bde9a879b")

    def __str__(self):
        return f"{self.id}) {self.nickname}"
    
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    is_active = models.BooleanField(default=False)    
    is_admin = models.BooleanField(default=False)    
    is_superuser = models.BooleanField(default=False)    
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['nickname', 'email']


    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    # @property
    # def is_active(self):
    #     "Is the user activate"
    #     # Simplest possible answer: All admins are staff
    #     return self.is_active


### Terms 약관
class Terms(models.Model):
    user = models.OneToOneField(BillrunUser, on_delete=models.CASCADE)
    service = models.DateTimeField(null= True, default=None)
    privacy = models.DateTimeField(null= True, default=None)
    location = models.DateTimeField(null= True, default=None)
    marketing = models.DateTimeField(null= True, blank=True, default=None)

    def __str__(self):
        return(f"{self.user}")


class Product(models.Model):
    DEFAULT_PK=1
    PRICEPROP = (
        ('Day', '일 당'),
        ('1h', '시간 당'),
        ('1w', '주당'),
    )
    GROUP = (
        ('woman', '여성의류/잡화'),
        ('man', '남성의류/잡화'),
        ('digital', '디지털/가전'),
        ('majorBook', '전공도서'),
        ('majorEtc', '전공기타'),
        ('game', '게임'),
        ('sports', '스포츠'),
        ('household', '생활잡화'),
        ('etc', '기타'),
    )

    lend = models.BooleanField(default=True)
    category = models.CharField(max_length=10, choices=GROUP)
    name = models.CharField(max_length=50)
    description = models.TextField()
    caution = models.TextField()
    price = models.IntegerField()
    price_prop = models.CharField(max_length=10, choices=PRICEPROP)
    hits = models.IntegerField(default=0)
    like_count = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(BillrunUser, null=True, default=DEFAULT_PK, on_delete=models.SET_NULL)
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, default=37.55723) #위도
    lng = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, default=127.04539) #경도
    location = models.CharField(max_length=50, default='', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add = True, null= True)
    updated_at = models.DateTimeField(auto_now = True, null= True)
    
    def upload_photo(self, filename):
        ymd_path = timezone.now().strftime('%Y/%m/')
        uuid_name = uuid4().hex
        extension = os.path.splitext(filename)[-1].lower()
        path = f'{ymd_path}/photo/{uuid_name + extension}'
        return path

    # def set_default(self, url):
    #     url_list = url.split('%2F')
    #     # url_quote = quote(url_list[1], safe='')
    #     full_url = f'{url_list[0]}%2F{url_list[1]}'
    #     return 
        
    photo1 = models.CharField(max_length=200, default="default%2Fno_image.png?alt=media&token=63b79d71-65a3-4706-b9f2-23d65503e288")
    photo2 = models.CharField(max_length=200, null=True, blank=True)
    photo3 = models.CharField(max_length=200, null=True, blank=True)
    photo4 = models.CharField(max_length=200, null=True, blank=True)
    photo5 = models.CharField(max_length=200, null=True, blank=True)

    # photo1 = models.ImageField(upload_to=upload_photo, default=photo_default)
    # photo2 = models.ImageField(upload_to=upload_photo, null=True, blank=True)
    # photo3 = models.ImageField(upload_to=upload_photo, null=True, blank=True)
    # photo4 = models.ImageField(upload_to=upload_photo, null=True, blank=True)
    # photo5 = models.ImageField(upload_to=upload_photo, null=True, blank=True)

    def __str__(self):
        if self.lend:
            return f"{self.id}) [빌려드림]{self.name}"
        else:
            return f"{self.id}) [빌림]{self.name}"


# class ProductPhoto(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="photos")
    
#     def upload_photo(self, filename):
#         ymd_path = timezone.now().strftime('%Y/%m/')
#         uuid_name = uuid4().hex
#         extension = os.path.splitext(filename)[-1].lower()
#         path = f'{ymd_path}/photo/{uuid_name + extension}'
#         return path
        
#     photo = models.ImageField(upload_to=upload_photo, null=True, blank=True, default=photo_default)

#     def __str__(self):
#         return f"{self.product}"
    

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
    user = models.ForeignKey(BillrunUser, null=True,  default=DEFAULT_PK, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)

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
# class Review(models.Model):
#     DEFAULT_PK=1
#     post = models.TextField()
#     product_score = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
#     user_score = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
#     deal = models.ForeignKey(Deal, default=DEFAULT_PK, on_delete=models.CASCADE)
#     # user = models.ForeignKey(User, default=DEFAULT_PK, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, default=DEFAULT_PK, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add = True, null= True)
#     updated_at = models.DateTimeField(auto_now = True, null= True)

#     def __str__(self):
#         return f"{self.deal.id}) {self.product.name} - {self.user.nickname}"

#     def upload_review(self, filename):
#         path = 'review/{}'.format(filename)
#         return path

#     photo = models.ImageField(upload_to=upload_review, null=True, blank=True)

class DealReview(models.Model):
    DEFAULT_PK=1
    SCOREPROP = (
        ('X', 'X'),
        ('상', '상'),
        ('중', '중'),
        ('하', '하'),
    )
    q1 = models.CharField(max_length=30, default=1, choices=SCOREPROP)
    q2 = models.CharField(max_length=30, default=1, choices=SCOREPROP)
    q3 = models.CharField(max_length=30, default=1, null=True, choices=SCOREPROP)
    q4 = models.CharField(max_length=30, default=1, null=True, choices=SCOREPROP)
    deal = models.ForeignKey(Deal, null=True, on_delete=models.CASCADE) #거래가 사라지면 거래리뷰도 사라진다. (필요X)
    user = models.ForeignKey(BillrunUser, null=True, default=DEFAULT_PK, on_delete=models.SET_NULL) #리뷰작성자
    created_at = models.DateTimeField(auto_now_add = True, null= True)
    updated_at = models.DateTimeField(auto_now = True, null= True)

    # def __str__(self):
    #     return f"{self.user.nickname} - {self.deal}"
    def __str__(self):
        return f"{self.deal} - {self.user.nickname}"

class ProductReview(models.Model):
    DEFAULT_PK=1
    score = models.FloatField(validators=[MinValueValidator(0.5), MaxValueValidator(5)])
    content = models.TextField()
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE)
    user = models.ForeignKey(BillrunUser, null=True, default=DEFAULT_PK, on_delete=models.SET_NULL) #유저가 삭제되어도 물품 리뷰는 남아있다.
    created_at = models.DateTimeField(auto_now_add = True, null= True)
    updated_at = models.DateTimeField(auto_now = True, null= True)

    # def __str__(self):
    #     return f"{self.user.nickname} - {self.deal.product.name}"
    def __str__(self):
        return f"{self.deal.product.name} - {self.user.nickname}"

class Favorite(models.Model):
    DEFAULT_PK=1
    user = models.ForeignKey(BillrunUser, default=DEFAULT_PK, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product, blank=True)
    created_at = models.DateTimeField(auto_now_add = True, null= True)
    updated_at = models.DateTimeField(auto_now = True, null= True)

    def __str__(self):
        return f"{self.user.nickname}의 찜 목록"

class Notice(models.Model):
    DEFAULT_PK=1
    user = models.ForeignKey(BillrunUser, default=DEFAULT_PK, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=50)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True, null= True)
    updated_at = models.DateTimeField(auto_now = True, null= True)
    
    def upload_banner(self, filename):
        ymd_path = timezone.now().strftime('%Y/%m/')
        uuid_name = uuid4().hex
        extension = os.path.splitext(filename)[-1].lower()
        path = f'{ymd_path}/notice/banner/{uuid_name + extension}'
        return path

    def upload_contentphoto(self, filename):
        ymd_path = timezone.now().strftime('%Y/%m/')
        uuid_name = uuid4().hex
        extension = os.path.splitext(filename)[-1].lower()
        path = f'{ymd_path}/notice/content/{uuid_name + extension}'
        return path

    def __str__(self):
        return f"{self.id}) {self.title}"
    banner_photo = models.ImageField(upload_to=upload_banner)
    content_photo = models.ImageField(upload_to=upload_contentphoto, null=True, blank=True)

class ChatRoom(models.Model):
    from_user = models.ForeignKey(BillrunUser, on_delete=models.SET_NULL, null= True, related_name= "from_rooms")
    to_user = models.ForeignKey(BillrunUser, on_delete=models.SET_NULL, null= True, related_name= "to_rooms")
    created_at = models.DateTimeField(auto_now_add = True)

class Chat(models.Model):
    user = models.ForeignKey(BillrunUser, on_delete= models.SET_NULL, null= True, related_name= "chats")
    room = models.ForeignKey(ChatRoom, on_delete= models.CASCADE, related_name= "chats")
    message = models.TextField(null= True, blank= True)
    created_at = models.DateTimeField(auto_now_add = True)
