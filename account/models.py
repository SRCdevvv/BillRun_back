from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.backends import ModelBackend
import random
from .secret import *

profile_default = 'user/default_user.png'


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, phone, community, email, nickname, lat, lng, password=None):
        if not phone:
            raise ValueError('핸드폰 번호를 입력해주세요.')
        n = random.randrange(1000,9999)
        nick = "빌런" + n
        #TODO 중복체크추가할것
        user = self.model(
            phone = fernet.encrypt(phone.encode()),
            community = community,
            email = self.noralize_email(email),
            # nickname = nick,
            nickname = nickname,
            lat = lat,
            lng = lng
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, nickname, password):
        user = self.create_user(
            nickname = nickname,
            password = password
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class BillRunUser(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()
    Group = (
        ('한양', '한양대학교'),
        # ('가천', '가천대학교'),
        # ('동국', '동국대학교'),
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

    is_active = models.BooleanField(default=False)    
    is_admin = models.BooleanField(default=False)    
    is_superuser = models.BooleanField(default=False)    
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'nickname'    
    REQUIRED_FIELDS = ['nickname']
