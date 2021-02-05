from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class User(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=10, default='', unique=True)
    money = models.IntegerField(default=0)
    level = models.CharField(max_length=10, default='', null=True, blank=True)
    place = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.id}) {self.nickname}({self.user.username})"


class Product(models.Model):
    DEFAULT_PK=1
    PRICEPROP = (
        ('Day', 'Per Day'),
        ('30m', 'Per half hour'),
        ('1h', 'Per hour'),
    )
    DEALOP = (
        ('F2F', 'Face to Face'),
        ('Untact', 'Untact'),
    )
    category = models.BooleanField(default=True)
    name = models.CharField(max_length=50)
    description = models.TextField()
    caution = models.TextField()
    price = models.IntegerField()
    price_prop = models.CharField(max_length=10, choices=PRICEPROP)
    place_option = models.BooleanField(default=True)
    deal_option = models.CharField(max_length=10, null=True, blank=True, default="", choices=DEALOP)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def upload_photo(self, filename):
        path = 'api/photo/{}'.format(filename)
        return path

    photo = models.ImageField(upload_to=upload_photo, null=True, blank=True)

    def __str__(self):
        if self.category:
            return f"{self.id}) [빌려드림]{self.name} - {self.user_id.nickname}"
        else:
            return f"{self.id}) [빌림]{self.name} - {self.user_id.nickname}"


class Deal(models.Model):
    DEALPROP = (
        ('Not', 'Not Yet'),
        ('PRO', 'In Progress'),
        ('COM', 'Complete'),
    )
    DEALOP = (
        ('F2F', 'Face to Face'),
        ('Untact', 'Untact'),
    )
    deal_prop = models.CharField(max_length=10, choices=DEALPROP)
    contract = models.BooleanField(default=False)
    contract2 = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    datentime = models.DateTimeField(auto_now=False, blank=False, null=False)
    period = models.IntegerField()
    deal_option = models.CharField(max_length=10, default="", choices=DEALOP)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        if self.product_id.category:
            return f"{self.id}) [빌려드림]{self.product_id.name} ({self.product_id.user_id.nickname} >> {self.user_id.nickname})"
        else:
            return f"{self.id}) [빌림]{self.product_id.name} ({self.product_id.user_id.nickname} >> {self.user_id.nickname})"


class Review(models.Model):
    post = models.TextField()
    product_score = models.FloatField()
    user_score = models.FloatField()
    deal_id = models.ForeignKey(Deal, default=False, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, default=False, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, default=Product.DEFAULT_PK, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.deal_id.id}) {self.product_id.name} - {self.user_id.nickname}"


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product, blank=True)

    def __str__(self):
        return f"{self.user.nickname}의 찜 목록"
