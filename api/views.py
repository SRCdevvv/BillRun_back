from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *

# Create your views here.
#### User
class UserList(APIView):
    def get(self, request):
        model = User.objects.all()
        serializer = UserSerializer(model, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

## 마이페이지
# 리뷰의 유저점수에서 평균을 내 빌런지수 보여주기(level)
# 빌려줘서 번 돈 ##########
# 찜 목록(Favorite)
# 유저의 거래 내역(Deal) - 대면/비대면 필터링


class UserDetail(APIView): #마이페이지

    def get_user(self, user_id): #특정 유저 가져오기
        try:
            model = User.objects.get(id=user_id)

            ##내가 빌려준 거래의 상품들 가져오기(거래완료 상태!!)
            #빌려드림에서 내가 올린 상품
            p1 = Product.objects.filter(user_id_id=model.id, category=True, deal__deal_prop='COM')
            #빌림에서 내가 빌려준 상품
            p2 = Product.objects.filter(deal__user_id=model.id, category=False, deal__deal_prop='COM')

            value = 0
            for x in p1:
                value += x.price
            for y in p2:
                value += x.price

            model.money = value
            model.save()
            return model
        except User.DoesNotExist:
            return

    # def sum_price(self, request, user_id):
    #     if not self.get_user(user_id):
    #         return Response(f'User with {user_id} is Not Found in database', status=status.HTTP_404_NOT_FOUND)
    #     serializer = UserSerializer(self.get_user(user_id), data=request.data)
    #     if serializer.is_valid():
    #         serializer.object.level = 
    #         serializer.save()
    #         return Response (serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

    def get(self, request, user_id):
        if not self.get_user(user_id):
            return Response(f'User with {user_id} is Not Found in database', status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(self.get_user(user_id))
        return Response(serializer.data)

    def put(self, request, user_id):
        if not self.get_user(user_id):
            return Response(f'User with {user_id} is Not Found in database', status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(self.get_user(user_id), data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response (serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

    def delete(self, request, user_id):
        if not self.get_user(user_id):
            return Response(f'User with {user_id} is Not Found in database', status=status.HTTP_404_NOT_FOUND)
        model = self.get_user(user_id)
        model.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserDetail_LendList(APIView): #마이페이지_빌려드림 거래목록
    def get(self, request, user_id):
        model = User.objects.get(id=user_id)
        # deals_a = Deal.objects.filter(user_id_id= user_id)
        return Response(serializer.data)



#### Product
class LendProductList(APIView): #빌려주는 상품 목록
    def get(self, request):
        model = Product.objects.filter(category=True)
        serializer = ProductSerializer(model, many=True)
        return Response(serializer.data)

class RentProductList(APIView): #빌리는 상품 목록
    def get(self, request):
        model = Product.objects.filter(category=False)
        serializer = ProductSerializer(model, many=True)
        return Response(serializer.data)

class ProductList(APIView): #전체 상품 목록 (이건 그냥 개발시 참고용!)
    def get(self, request):
        model = Product.objects.all()
        serializer = ProductSerializer(model, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class ProductDetail(APIView): #상품 상세보기
    def get_product(self, product_id):
        try:
            model = Product.objects.get(id=product_id)
            return model
        except Product.DoesNotExist:
            return

    def get(self, request, product_id):
        if not self.get_product(product_id):
            return Response(f'Product with {product_id} is Not Found in database', status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(self.get_product(product_id))
        return Response(serializer.data)

        #상품에 대한 리뷰 불러오기 추가!!!!!!!!!!!


    def put(self, request, product_id):
        if not self.get_product(product_id):
            return Response(f'Product with {product_id} is Not Found in database', status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(self.get_product(product_id), data=request.data)
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
        serializer = DealSerializer(model, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DealSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    
class DealDetail(APIView): #거래 수정(완료로)
    def get_deal(self, deal_id):
        try:
            model = Deal.objects.get(id=deal_id)
            return model
        except Deal.DoesNotExist:
            return

    def get(self, request, deal_id):
        if not self.get_deal(deal_id):
            return Response(f'Deal with {deal_id} is Not Found in database', status=status.HTTP_404_NOT_FOUND)
        serializer = DealSerializer(self.get_deal(deal_id))
        return Response(serializer.data)

    def put(self, request, deal_id):
        if not self.get_deal(deal_id):
            return Response(f'Deal with {deal_id} is Not Found in database', status=status.HTTP_404_NOT_FOUND)
        serializer = DealSerializer(self.get_deal(deal_id), data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 


#본인의 거래 내역

#특정 거래 내역 보기

#거래상태 완료 시 계약서 삭제


#### Review - 거래 먼저 하자...
#거래에 대한 리뷰 작성 - 해당 거래의 유저들만 리뷰 한번만! 작성 가능
#상품, 유저점수는 0.5~5로 0.5단위

class ReviewList(APIView): #상품 목록 (이건 그냥 개발시 참고용!)
    def post(self, request):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


#### Favorite