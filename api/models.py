from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class User(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    place = models.CharField(max_length=50)

class Product(models.Model):
    PRICE_PROP = (
        ('Day', 'Per Day'),
        ('30m', 'Per half hour'),
        ('1h', 'Per hour'),
    )
    category = models.BooleanField(default=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    caution = models.CharField(max_length=300)
    price = models.IntegerField()
    price_prop = models.CharField(max_length=10, choices=PRICE_PROP)
    place_option = models.BooleanField(default=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def upload_photo(self, filename):
        path = 'api/photo/{}'.format(filename)
        return path

    photo = models.ImageField(upload_to=upload_photo, null=True, blank=True)

class Review(models.Model):
    post = models.CharField(max_length=300)
    product_score = models.FloatField()
    user_score = models.FloatField()
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

class Trade(models.Model):
    TRADE_PROP = (
        ('Not', 'Not Yet'),
        ('PRO', 'In Progress'),
        ('COM', 'Complete'),
    )
    price_prop = models.CharField(max_length=10, choices=TRADE_PROP)
    contract = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    datentime = models.DateTimeField(auto_now=False, blank=False, null=False)
    period = models.IntegerField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    





