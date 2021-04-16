from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.utils import timezone

profile_default = 'user/default_user.png'
photo_default = 'photo/no_image.png'

# Create your models here.
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
