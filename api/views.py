from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .serializers import *
from .models import *

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

import json

# main page
def main(request):
    return render(request, 'api/main.html')

### Auth
# def	make_signature():
# 	timestamp = int(time.time() * 1000)
# 	timestamp = str(timestamp)

# 	access_key = ACCESS_KEY			# access key id (from portal or Sub Account)
# 	secret_key = SECRET_KEY				# secret key (from portal or Sub Account)
# 	secret_key = bytes(secret_key, 'UTF-8')

# 	method = "GET"
# 	uri = "/sms/v2/services/{SERVICE_ID}/messages"

# 	message = method + " " + uri + "\n" + timestamp + "\n" + access_key
# 	message = bytes(message, 'UTF-8')
# 	signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
# 	return signingKey

class SMSVerification(APIView):
    def post(self, request):
        try:
            data = json.loads(request.body)
            AuthSms.objects.update_or_create(phone_number=data['phone_number'])
            # sms = AuthSms.objects.get(phone_number=data['phone_number'])
            # AuthSms.send_sms(sms)
            # AuthSms.test(sms)
            return Response({'message': 'OK', 'status': Response.status_code})
        except KeyError:
            return Response({'message': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)

class SMSConfirm(APIView):
    def post(self, request):
        try:
            data = json.loads(request.body)
            phone = data['phone_number']
            verification_number = data['auth_number']
            if verification_number == AuthSms.objects.get(phone_number=phone).auth_number:
                if not User.objects.filter(phone=phone).exists():
                    # User.objects.create(phone=phone)
                    # 여기서 유저를 만들어야하는데 유저부터 수정하자!
                    return Response({'message': 'SUCCESS'}, status=200)
                else:
                    return Response({'message': 'REGISTERED_NUMBER'}, status=401)
            return Response({'message': 'INVALID_NUMBER'}, status=401)
        except KeyError as e:
            return Response({'message': f'KEY_ERROR: {e}'}, status=400)

        except ValueError as e:
            return Response({'message': f'VALUE_ERROR: {e}'}, status=400)


#### User
# class UserList(APIView): #전체 유저 리스트
#     def get(self, request):
#         model = User.objects.all()
#         # serializer = UserSerializer(model, many=True)
#         serializer = UserSerializer(model, context={'request': request}, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

## 마이페이지
# 리뷰의 유저점수에서 평균을 내 빌런지수 보여주기(level)
# 찜 목록(Favorite)
# 유저의 거래 내역(Deal) - 대면/비대면 필터링
# 유저의 리뷰 내력(받은거)

# class UserDetail(APIView): #마이페이지
#     def get_user(self, user_id): #특정 유저 가져오기
#         try:
#             model = User.objects.get(id=user_id)

#             value = 0
#             ##내가 빌려준 거래의 상품들 가져오기(거래완료 상태!!)
#             #빌려드림에서 내가 올린 상품의 금액
#             for x in Product.objects.filter(user=model.id, lend=True, deal__deal_prop='COM'): #_id 수정해봤는데 값 잘 나오네요
#                 # period = 
#                 value += x.price
#             #빌림에서 내가 빌려준 상품의 금액
#             for y in Product.objects.filter(deal__user=model.id, lend=False, deal__deal_prop='COM'): #_id 수정해봤는데 값 잘 나오네요
#                 value += y.price

#             model.money = value #내가 번 돈 저장
#             model.save()
#             return model
#         except User.DoesNotExist:
#             return

#     # def sum_price(self, request, user_id):
#     #     if not self.get_user(user_id):
#     #         return Response(f'User with {user_id} is Not Found in database', status=status.HTTP_404_NOT_FOUND)
#     #     serializer = UserSerializer(self.get_user(user_id), data=request.data)
#     #     if serializer.is_valid():
#     #         serializer.object.level = 
#     #         serializer.save()
#     #         return Response (serializer.data, status=status.HTTP_201_CREATED)
#     #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

#     def get(self, request, user_id):
#         if not self.get_user(user_id):
#             return Response(f'User with {user_id} is Not Found in database', status=status.HTTP_404_NOT_FOUND)
#         serializer = UserSerializer(self.get_user(user_id), context={'request': request})
#         return Response(serializer.data)

#     def put(self, request, user_id):
#         if not self.get_user(user_id):
#             return Response(f'User with {user_id} is Not Found in database', status=status.HTTP_404_NOT_FOUND)
#         serializer = UserSerializer(self.get_user(user_id), data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

#     def delete(self, request, user_id):
#         if not self.get_user(user_id):
#             return Response(f'User with {user_id} is Not Found in database', status=status.HTTP_404_NOT_FOUND)
#         model = self.get_user(user_id)
#         model.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# class UserDetail_LendList(APIView): #마이페이지_빌려드림 거래목록. 아직 사용 안했고 추후 수정해야함!
#     def get(self, request, user_id):
#         model = User.objects.get(id=user_id)
#         # deals_a = Deal.objects.filter(user_id_id= user_id)
#         # serializer = UserSerializer(model)
#         return Response(serializer.data)

#### New User
class UserCreate(generics.CreateAPIView): #회원가입
    queryset = BillrunUser.objects.all()
    serializer_class = UserCreateSerializer

# class UserLogin(generics.RetrieveUpdateDestroyAPIView):
#     def get(self, request):
#         serializer = UserLoginSerializer(data=request.data)
#         if not serializer.is_valid(raise_exception=True):
#             return Response({"message":"Request Body Error."}, status=status.HTTP_409_CONFLICT)
#         if serializer.validated_data['phone'] == "None":
#             return Response({"message": "fail"}, status=status.HTTP_200_OK)
        
#         response = {
#             'success': 'True',
#             'token': serializer.data['token']
#         }
#         return Response(response, status=status.HTTP_200_OK)

#{"phone":"01066278667"}
#로그인
@api_view(['POST'])
@permission_classes([AllowAny])
def signin(request):
    if request.method == 'POST':
        serializer = UserLoginSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response({"message":"Request Body Error."}, status=status.HTTP_409_CONFLICT)
        if serializer.validated_data['phone'] == "None":
            return Response({"message": "fail"}, status=status.HTTP_200_OK)
        
        response = {
            'success': 'True',
            'token': serializer.data['token']
        }
        return Response(response, status=status.HTTP_200_OK)


#### Product
class LendProductList(APIView): #빌려주는 상품 목록
    def get(self, request):
        model = Product.objects.filter(lend=True)
        serializer = ProductSerializer(model, context={'request': request}, many=True)
        return Response(serializer.data)

class RentProductList(APIView): #빌리는 상품 목록
    def get(self, request):
        model = Product.objects.filter(lend=False)
        serializer = ProductSerializer(model, context={'request': request}, many=True)
        return Response(serializer.data)

class ProductList(APIView): #전체 상품 목록 (이건 그냥 개발시 참고용!)
    def get(self, request):
        model = Product.objects.all()
        serializer = ProductSerializer(model, context={'request': request}, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class UserLendProductList(APIView): #특정 유저가 빌려주는 물품 리스트
    def get_product(self, user_id):
        try:
            model = Product.objects.filter(user=user_id, lend=True)
            return model
        except Product.DoesNotExist:
            return

    def get(self, request, user_id):
        if not self.get_product(user_id):
            return Response(f'Lend Product with User ID {user_id} is Not Found in database', status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(self.get_product(user_id), context={'request': request}, many=True)
        return Response(serializer.data)

class UserRentProductList(APIView): #특정 유저가 빌리는 물품 리스트
    def get_product(self, user_id): 
        try:
            model = Product.objects.filter(user=user_id, lend=False)
            return model
        except Product.DoesNotExist:
            return

    def get(self, request, user_id):
        if not self.get_product(user_id):
            return Response(f'Rent Product with User ID {user_id} is Not Found in database', status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(self.get_product(user_id), context={'request': request}, many=True)
        return Response(serializer.data)

class ProductDetail(APIView): #상품 상세보기
    def get_product(self, product_id):
        try:
            model = Product.objects.get(id=product_id)
            model.hits += 1
            model.save()
            return model
        except Product.DoesNotExist:
            return

    def get(self, request, product_id):
        p = self.get_product(product_id)
        # if not self.get_product(product_id):
        if not p:
            return Response(f'Product with {product_id} is Not Found in database', status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(p, context={'request': request})
        return Response(serializer.data)

        #상품에 대한 리뷰 불러오기 추가!!!!!!!!!!!


    def put(self, request, product_id):
        if not self.get_product(product_id):
            return Response(f'Product with {product_id} is Not Found in database', status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(self.get_product(product_id), context={'request': request}, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

    def delete(self, request, product_id):
        if not self.get_product(product_id):
            return Response(f'Product with {product_id} is Not Found in database', status=status.HTTP_404_NOT_FOUND)
        model = self.get_product(product_id)
        model.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



#### Deal
class DealList(APIView): 
    def get(self, request): #전체 거래 목록
        model = Deal.objects.all()
        serializer = DealSerializer(model, context={'request': request}, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DealSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class DealDetail(APIView): #거래 상세보기
    def get_deal(self, deal_id):
            try:
                model = Deal.objects.get(id=deal_id)
                return model
            except Deal.DoesNotExist:
                return

    def get(self, request, deal_id):
        if not self.get_deal(deal_id):
            return Response(f'Deal with ID {deal_id} is Not Found in database', status=status.HTTP_404_NOT_FOUND)
        serializer = DealSerializer(self.get_deal(deal_id), context={'request': request})
        return Response(serializer.data)

    def put(self, request, deal_id):
        if not self.get_deal(deal_id):
            return Response(f'Deal with User ID {deal_id} is Not Found in database', status=status.HTTP_404_NOT_FOUND)
        serializer = DealSerializer(self.get_deal(deal_id), context={'request': request}, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    
class LendDealList(APIView): #특정 유저의 빌려준 거래 리스트
    def get_deal(self, user_id):
        try:
            # model = Deal.objects.get(id=user_id)
            model = Deal.objects.filter(Q(user=user_id, product__lend=False) | Q(product__user=user_id, product__lend=True))
            return model
        except Deal.DoesNotExist:
            return

    def get(self, request, user_id):
        if not self.get_deal(user_id):
            return Response(f'Deal with User ID {user_id} is Not Found in database', status=status.HTTP_404_NOT_FOUND)
        serializer = DealSerializer(self.get_deal(user_id), context={'request': request}, many=True)
        return Response(serializer.data)

class RentDealList(APIView): #특정 유저가 빌린 거래 리스트
    def get_deal(self, user_id): 
        try:
            # model = Deal.objects.get(id=user_id)
            model = Deal.objects.filter(Q(user=user_id, product__lend=True) | Q(product__user=user_id, product__lend=False))
            return model
        except Deal.DoesNotExist:
            return

    def get(self, request, user_id):
        if not self.get_deal(user_id):
            return Response(f'Deal with User ID {user_id} is Not Found in database', status=status.HTTP_404_NOT_FOUND)
        serializer = DealSerializer(self.get_deal(user_id), context={'request': request}, many=True)
        return Response(serializer.data)


#### Review
#거래에 대한 리뷰 작성 - 해당 거래의 유저들만 리뷰 한번만! 작성 가능
#상품, 유저점수는 0.5~5로 0.5단위

class ReviewList(APIView): #리뷰 목록 (이건 그냥 개발시 참고용!)
    def get(self, request): #전체 리뷰 목록
        model = Review.objects.all()
        serializer = ReviewSerializer(model, many=True)
        return Response(serializer.data)

    def post(self, request): #리뷰 남기기
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            # serializer.object.product_id.user_id.id
            # serializer.object.deal_id.user_id.id
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DealReviewPost(APIView):
    def post(self, request): #거래 리뷰 작성
        serializer = DealReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    ##거래에 참여한 2인만이 쓸 수 있다!!!!!!!!!!!!! 추가할것

class UserReviewDetail(APIView): #특정 유저에 대한 리뷰 가져오기
    def get_dealreview(self, user_id):
        try:
            model = DealReview.objects.filter(Q(Q(deal__user=user_id)|Q(deal__product__user=user_id)) & ~Q(user = user_id))
            return model
        except DealReview.DoesNotExist:
            return
    
    def get(self, request, user_id):
        if not self.get_dealreview(user_id):
            return Response(f'DealReivew with User ID {user_id} is Not Found in database', status=status.HTTP_404_NOT_FOUND)
        serializer = DealReviewSerializer(self.get_dealreview(user_id), context={'request': request}, many=True)
        return Response(serializer.data)

class ProductReviewPost(APIView): #물품 리뷰 작성
    def post(self, request): #물품 리뷰 작성
        serializer = ProductReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    ##거래에 참여한 2인만이 쓸 수 있다!!!!!!!!!!!!! 추가할것

class ProductReviewDetail(APIView): #특정 물품에 대한 리뷰 가져오기
    def get_pro_review(self, product_id):
        try:
            model = ProductReview.objects.filter(deal__product__id=product_id)
            return model
        except ProductReview.DoesNotExist:
            return
    
    def get(self, request, product_id):
        if not self.get_pro_review(product_id):
            return Response(f'ProductReivew with ID {product_id} is Not Found in database', status=status.HTTP_404_NOT_FOUND)
        serializer = ProductReviewSerializer(self.get_pro_review(product_id), context={'request': request}, many=True)
        return Response(serializer.data)

###이전리뷰
class ReviewDetail(APIView): #특정 상품에 대한 리뷰 가져오기
    def get_review(self, product_id):
        try:
            # 현재 로그인한 유저가 이 둘 중 하나라면 리뷰 작성할 수 있도록. 아닐 경우 권한이 없습니다.
            # 추후 작성
            # deal = Deal.objects.get(id=deal_id)
            # user1 = User.objects.get(id=deal.user_id.id) #거래에 참여한 사람
            # user2 = User.objects.get(id=deal.product_id.user_id.id) #상품을 올린 사람

            # 이 상품의 카테고리
            # if deal.product_id.category:
            #     return #user1이 빌리는 사람, user2가 빌려주는 사람
            # else:
            #     return #user1이 빌려주는 사람, user2가 빌리는 사람
            
            # product = Product.objects.get(id=product_id)
            # model = Review.objects.filter(deal_id_product_id_id=product_id)
            
            model = Review.objects.filter(product_id=product_id)
            return model
        except Review.DoesNotExist:
            return

    def get(self, request, product_id):
        if not self.get_review(product_id):
            return Response(f'Review with Product id {product_id} is Not Found in database', status=status.HTTP_404_NOT_FOUND)
        serializer = ReviewSerializer(self.get_review(product_id), many=True)
        return Response(serializer.data)

    def put(self, request, product_id):
        if not self.get_review(product_id):
            return Response(f'Review with Product id {product_id} is Not Found in database', status=status.HTTP_404_NOT_FOUND)
        serializer = ReviewSerializer(self.get_review(product_id), data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

#### Favorite
def product_like_toggle(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    # user = request.user
    # profile = Profile.objects.get(user=user)
    # check_like_product = profile.like_products.filter(id=product_id)

    # if check_like_post.exists():
    #     profile.like_posts.remove(post)
    #     product.like_count -= 1
    #     post.save()
    # else:
    #     profile.like_posts.add(post)
    product.like_count += 1
    product.save()
    # return product

    return redirect('api:product_detail', product_id) #끝맺음을 어떻게 해야 할 지 모르겠구먼

class FavoriteList(APIView): #전체 좋아요 목록(이건 그냥 개발시 참고용!)
    def get(self, request): 
        model = Favorite.objects.all()
        serializer = FavoriteSerializer(model, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FavoriteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FavoriteDetail(APIView):
    def get_favorite(self, user_id):#특정 유저에 대한 좋아요 가져오기
        try:
            model = Favorite.objects.filter(user_id=user_id)
            return model
        except Review.DoesNotExist:
            return

    def get(self, request, user_id):
        if not self.get_favorite(user_id):
            return Response(f'Favorite with User id {user_id} is Not Found in database', status=status.HTTP_404_NOT_FOUND)
        serializer = FavoriteSerializer(self.get_favorite(user_id), many=True)
        return Response(serializer.data)

    def put(self, request, user_id):
        if not self.get_favorite(user_id):
            return Response(f'Favorite with User id {user_id} is Not Found in database', status=status.HTTP_404_NOT_FOUND)
        serializer = FavoriteSerializer(self.get_favorite(user_id), data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

#### Notice
class NoticeList(APIView):
    def get(self, request): 
        model = Notice.objects.all()
        serializer = NoticeSerializer(model, context={'request': request}, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = NoticeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NoticeDetail(APIView): #이벤트 상세보기
    def get_notice(self, notice_id):
        try:
            model = Notice.objects.get(id=notice_id)
            return model
        except Notice.DoesNotExist:
            return

    def get(self, request, notice_id):
        if not self.get_notice(notice_id):
            return Response(f'Notice with {notice_id} is Not Found in database', status=status.HTTP_404_NOT_FOUND)
        serializer = NoticeSerializer(self.get_notice(notice_id), context={'request': request})
        return Response(serializer.data)

    def put(self, request, notice_id):
        if not self.get_notice(notice_id):
            return Response(f'Notice with {notice_id} is Not Found in database', status=status.HTTP_404_NOT_FOUND)
        serializer = NoticeSerializer(self.get_notice(notice_id), context={'request': request}, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

    def delete(self, request, notice_id):
        if not self.get_notice(notice_id):
            return Response(f'Notice with {notice_id} is Not Found in database', status=status.HTTP_404_NOT_FOUND)
        model = self.get_notice(notice_id)
        model.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)