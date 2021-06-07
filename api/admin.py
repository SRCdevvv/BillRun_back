from django.contrib import admin
from .models import *
from BillRun_back.admin import admin_site

class PhotoInline(admin.TabularInline):
    model = ProductPhoto

class ProductAdmin(admin.ModelAdmin):
    inlines = [PhotoInline, ]

admin_site.register(Product, ProductAdmin)
admin_site.register(Review)
admin_site.register(DealReview)
admin_site.register(ProductReview)
admin_site.register(Deal)
admin_site.register(Favorite)
admin_site.register(Notice)
admin_site.register(AuthSms)
admin_site.register(Terms)

class UserAdmin(admin.ModelAdmin):
    list_display = (
        'nickname',
        'email',
        'community',
        # 'date_joined'
    )

    list_display_links = (
        'nickname',
        'email'
    )

admin_site.register(BillrunUser, UserAdmin)


