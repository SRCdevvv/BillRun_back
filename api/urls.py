from django.urls import path
from .views import *

urlpatterns = [
    path('user_list/', UserList.as_view(), name="user_list"),
    path('user_list/<int:user_id>', UserDetail.as_view(), name="user_detail"),

    #빌려드림
    path('lend_product_list/', LendProductList.as_view(), name="lend_product_list"),
    path('lend_product_list/<int:product_id>', ProductDetail.as_view(), name="lend_product_detail"),

    #빌림
    path('rent_product_list/', RentProductList.as_view(), name="rent_product_list"),
    path('rent_product_list/<int:product_id>', ProductDetail.as_view(), name="rent_product_detail"),

    #상품 전체보기(일단 만들어둠)
    path('product_list/', ProductList.as_view(), name="product_list"),
    # path('product_list/<int:product_id>', ProductDetail.as_view(), name="product_detail"),
]