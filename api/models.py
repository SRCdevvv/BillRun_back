from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class User(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    place = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user.username}"


class Product(models.Model):
    PRICEPROP = (
        ('Day', 'Per Day'),
        ('30m', 'Per half hour'),
        ('1h', 'Per hour'),
    )
    category = models.BooleanField(default=True)
    name = models.CharField(max_length=50)
    description = models.TextField()
    caution = models.TextField()
    price = models.IntegerField()
    price_prop = models.CharField(max_length=10, choices=PRICEPROP)
    place_option = models.BooleanField(default=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def upload_photo(self, filename):
        path = 'api/photo/{}'.format(filename)
        return path

    photo = models.ImageField(upload_to=upload_photo, null=True, blank=True)

    def __str__(self):
        return f"{self.name}"


class Deal(models.Model):
    DEALPROP = (
        ('Not', 'Not Yet'),
        ('PRO', 'In Progress'),
        ('COM', 'Complete'),
    )
    deal_prop = models.CharField(max_length=10, choices=DEALPROP)
    contract = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    datentime = models.DateTimeField(auto_now=False, blank=False, null=False)
    period = models.IntegerField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user_id.user.username} - {self.product_id.name}"


class Review(models.Model):
    post = models.TextField()
    product_score = models.FloatField()
    user_score = models.FloatField()
    deal_id = models.OneToOneField(Deal, default=False, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, default=False, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, default=False, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user_id.user.username} - {self.product_id.name}"