from django.urls import path, include
from rest_framework import urls
from rest_framework.routers import DefaultRouter
from .views import *
from django.conf.urls import url, static
from django.conf import settings

app_name='api'
router = DefaultRouter()
router.register('product', ProductViewSet)
router.register('lend', LendProductViewSet)
router.register('rent', RentProductViewSet)

urlpatterns = [
    ### Main
    path('', main, name="main"),
    path('main_user', main_user, name="main_user"),
    path('main_prodeal', main_prodeal, name="main_prodeal"),


    ### User
    path('user_list/', UserList.as_view(), name="user_list"),
    path('user_list/<int:user_id>', UserDetail.as_view(), name="user_detail"),


    ### Auth
    # 개발용 signin, signup
    path('signup/', UserCreate.as_view(), name="signup"),
    path('signin/', signin, name="signin"),
    # path('logout/', LogoutView.as_view(), name="logout"),

    # sms인증
    path('sms', SMSVerification.as_view(), name="sms"), #인증번호 전송
    path('sms_confirm', SMSConfirm.as_view(), name="sms_confirm"), #인증번호 확인

    # email인증
    path('email', EmailConfirm.as_view(), name="email"), #이메일 전송
    path('email/users/<str:uidb64>/<str:token>', activate), #유저 활성화
    path('user_active', activate_success, name="user_active"), #유저에게 활성화 완료 결과를 보여주는 페이지

    # Terms 약관동의
    path('terms/', TermsAgreement.as_view(), name="terms"),
    path('terms/<int:user_id>', UserTermsDetail.as_view(), name="terms_detail"), #유저의 약관동의 내역/일시 확인


    ### Product
    # 상품 등록
    path('product_post/', ProductPost.as_view(), name="product_post"),

    # 전체 상품 목록
    # path('product_list/', ProductList.as_view(), name="product_list"),
    # path('product_list/', product_list),
    path('product_list/', include(router.urls)),

    # 카테고리 별 상품 목록
    path('product/<str:ctgr>', ProductCategoryList.as_view(), name="product_ctgr"),

    # 물품 상세보기
    # path('product/<int:product_id>', ProductDetail.as_view(), name="product_detail"),
    # path('product/<int:product_id>', product_detail),

    # Lend 빌려드림
    # path('lend_product_list/', LendProductList.as_view(), name="lend_product_list"),
    # path('lend_product_list/<int:product_id>', ProductDetail.as_view(), name="lend_product_detail"), #물품 상세보기
    path('lend_product_list/user_id=<int:user_id>', UserLendProductList.as_view(), name="user_lend_product"), #특정 유저의 빌려드림 리스트
    
    # Rent 빌림
    # path('rent_product_list/', RentProductList.as_view(), name="rent_product_list"),
    # path('rent_product_list/<int:product_id>', ProductDetail.as_view(), name="rent_product_detail"), #물품 상세보기
    path('rent_product_list/user_id=<int:user_id>', UserRentProductList.as_view(), name="user_rent_product"), #특정 유저의 빌림 리스트

    # Like 좋아요 누르기 TODO 추가개발필요
    path('like/<int:product_id>', product_like_toggle, name="like_toggle"),


    ### Deal
    # 거래 진행
    path('deal_list/', DealList.as_view(), name="deal_list"),
    path('deal_list/<int:deal_id>', DealDetail.as_view(), name="deal_datail"),
    path('lend_deal_list/<int:user_id>', LendDealList.as_view(), name="lend_deal_list"),
    path('rent_deal_list/<int:user_id>', RentDealList.as_view(), name="rent_deal_list"),

    ### Review
    #물품리뷰 등록
    path('pro_review', ProductReviewPost.as_view(), name="pro_review"), 

    #특정 물품리뷰 상세보기
    path('review/pro_id=<int:product_id>', ProductReviewDetail.as_view(), name="pro_review_detail"), 

    #거래리뷰 등록(유저리뷰)
    path('deal_review', DealReviewPost.as_view(), name="deal_review"), 

    #특정 유저리뷰 상세보기
    path('review/user_id=<int:user_id>', UserReviewDetail.as_view(), name="user_review_detail"), 

    # Favorite 찜 목록
    path('favorite/', FavoriteList.as_view(), name="favorite_list"),
    path('favorite/<int:user_id>', FavoriteDetail.as_view(), name="favorite_detail"),

    # Notice 배너(공지사항, 이벤트)
    path('notice/', NoticeList.as_view(), name="notice"),
    path('notice/<int:notice_id>', NoticeDetail.as_view(), name="notice_detail"),
] 