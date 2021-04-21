from django.contrib import admin
from api.models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Product)
admin.site.register(Review)
admin.site.register(Deal)
admin.site.register(Favorite)
admin.site.register(Notice)

admin.site.register(AuthSms)