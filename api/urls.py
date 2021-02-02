from django.urls import path
from .views import *

urlpatterns = [
    path('user_list/', UserList.as_view(), name="user_list"),
    path('user_list/<int:user_id>', UserDetail.as_view(), name="user_detail"),
    path('product_list/', ProductList.as_view(), name="product_list"),
    path('product_list/<int:product_id>', ProductDetail.as_view(), name="product_detail"),
]