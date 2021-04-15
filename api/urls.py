from django.urls import path
from .views import *

app_name='api'
urlpatterns = [
    path('user_list/', UserList.as_view(), name="user_list"),
    path('user_list/<int:user_id>', UserDetail.as_view(), name="user_detail"),

    #빌려드림
    path('lend_product_list/', LendProductList.as_view(), name="lend_product_list"),
    path('lend_product_list/<int:product_id>', ProductDetail.as_view(), name="lend_product_detail"),
    
    #빌려드림 상품에 대한 리뷰 작성
    # path('lend_product_list/<int:product_id>/new_review', ReviewDetail.as_view(), name="new_review_lend"),

    #빌림
    path('rent_product_list/', RentProductList.as_view(), name="rent_product_list"),
    path('rent_product_list/<int:product_id>', ProductDetail.as_view(), name="rent_product_detail"),
    
    #빌림 상품에 대한 리뷰 작성
    # path('rent_product_list/<int:product_id>/new_review', ReviewDetail.as_view(), name="new_review_rent"),

    #상품 등록
    path('product_list/', ProductList.as_view(), name="product_list"),

    #전체 상품에서 상세보기(일단 만들어 놓음)
    path('product_list/<int:product_id>', ProductDetail.as_view(), name="product_detail"),

    #거래 진행
    path('deal_list/', DealList.as_view(), name="deal_list"),
    path('deal_list/<int:deal_id>', DealDetail.as_view(), name="deal_datail"),

    #리뷰
    path('review/', ReviewList.as_view(), name="review_list"),
    path('review/<int:product_id>', ReviewDetail.as_view(), name="review_detail"),


]