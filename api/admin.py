from django.contrib import admin
from api.models import *

# Register your models here.

class PhotoInline(admin.TabularInline):
    model = ProductPhoto

class ProductAdmin(admin.ModelAdmin):
    inlines = [PhotoInline, ]

admin.site.register(User)
admin.site.register(Product, ProductAdmin)
admin.site.register(Review)
admin.site.register(Deal)
admin.site.register(Favorite)
admin.site.register(Notice)
admin.site.register(AuthSms)