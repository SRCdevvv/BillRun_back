from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.backends import ModelBackend
import random

# Create your models here.
class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, phone, community, email, nickname, lat, lng, password=None):
        if not phone:
            raise ValueError('핸드폰 번호를 입력해주세요.')
        n = random.randrange(1000,9999)
        user = self.model(
            phone = phone,
            community = community,
            email = self.noralize_email(email),
            nickname = nickname,
            lat = lat,
            lng = lng
        )
        # user.set_password(password)
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
    community = models.CharField(max_length=50, choices=Group)
    email = models.EmailField(max_length=254, unique=True)
    nickname = models.CharField(max_length=20, unique=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6) #위도
    lng = models.DecimalField(max_digits=9, decimal_places=6) #경도
    
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    is_active = models.BooleanField(default=True)    
    is_admin = models.BooleanField(default=False)    
    is_superuser = models.BooleanField(default=False)    
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'nickname'    
    REQUIRED_FIELDS = ['nickname']
