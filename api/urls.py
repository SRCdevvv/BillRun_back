from django.urls import path, include
from rest_framework import urls
import rest_framework
from .views import *
from django.conf.urls import url, static
from django.conf import settings

app_name='api'
urlpatterns = [
    path('', main, name="main"),
    # path('user_list/', UserList.as_view(), name="user_list"),
    # path('user_list/<int:user_id>', UserDetail.as_view(), name="user_detail"),

    #Auth
    path('signup/', UserCreate.as_view()),
    path('login/', login),

    #빌려드림
    path('lend_product_list/', LendProductList.as_view(), name="lend_product_list"),
    path('lend_product_list/<int:product_id>', ProductDetail.as_view(), name="lend_product_detail"),
    path('lend_product_list/user_id=<int:user_id>', UserLendProductList.as_view(), name="user_lend_product"),
    
    #빌려드림 상품에 대한 리뷰 작성
    # path('lend_product_list/<int:product_id>/new_review', ReviewDetail.as_view(), name="new_review_lend"),

    #빌림
    path('rent_product_list/', RentProductList.as_view(), name="rent_product_list"),
    path('rent_product_list/<int:product_id>', ProductDetail.as_view(), name="rent_product_detail"),
    path('rent_product_list/user_id=<int:user_id>', UserRentProductList.as_view(), name="user_rent_product"),
    
    #빌림 상품에 대한 리뷰 작성
    # path('rent_product_list/<int:product_id>/new_review', ReviewDetail.as_view(), name="new_review_rent"),

    #상품 등록
    path('product_list/', ProductList.as_view(), name="product_list"),

    #전체 상품에서 상세보기(일단 만들어 놓음)
    path('product_list/<int:product_id>', ProductDetail.as_view(), name="product_detail"),

    #거래 진행
    path('deal_list/', DealList.as_view(), name="deal_list"),
    path('deal_list/<int:deal_id>', DealDetail.as_view(), name="deal_datail"),
    path('lend_deal_list/<int:user_id>', LendDealList.as_view(), name="lend_deal_list"),
    path('rent_deal_list/<int:user_id>', RentDealList.as_view(), name="rent_deal_list"),

    #리뷰
    path('review/', ReviewList.as_view(), name="review_list"),
    path('pro_review', ProductReviewPost.as_view(), name="pro_review"),
    path('deal_review', DealReviewPost.as_view(), name="deal_review"),
    path('review/<int:product_id>', ReviewDetail.as_view(), name="review_detail"), #이전리뷰
    path('review/pro_id=<int:product_id>', ProductReviewDetail.as_view(), name="pro_review_detail"), #물품리뷰
    path('review/user_id=<int:user_id>', UserReviewDetail.as_view(), name="user_review_detail"), #유저리뷰

    #좋아요 누르기
    path('like/<int:product_id>', product_like_toggle, name="like_toggle"),

    #찜 목록
    path('favorite/', FavoriteList.as_view(), name="favorite_list"),
    path('favorite/<int:user_id>', FavoriteDetail.as_view(), name="favorite_detail"),

    #배너(공지사항, 이벤트)
    path('notice/', NoticeList.as_view(), name="notice"),
    path('notice/<int:notice_id>', NoticeDetail.as_view(), name="notice_detail"),

    #api시험
    path('sms', SMSVerification.as_view(), name="sms"),
    path('sms_confirm', SMSConfirm.as_view(), name="sms_confirm"),
] 