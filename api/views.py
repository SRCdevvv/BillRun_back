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


class UserDetail(APIView):
    def get_user(self, user_id):
        try:
            model = User.objects.get(id=user_id)
            return model
        except User.DoesNotExist:
            return

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
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

    def delete(self, request, user_id):
        if not self.get_user(user_id):
            return Response(f'User with {user_id} is Not Found in database', status=status.HTTP_404_NOT_FOUND)
        model = self.get_user(user_id)
        model.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#### Product
class ProductList(APIView):
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


class ProductDetail(APIView):
    def get_product(self, product_id):
        try:
            model = Product.objects.get(id=product_id)
            return model
        except Product.DoesNotExist:
            return

    def get(self, request, product_id):
        if not self.get_product(product_id):
            return Response(f'User with {product_id} is Not Found in database', status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(self.get_product(product_id))
        return Response(serializer.data)

    def put(self, request, product_id):
        if not self.get_product(product_id):
            return Response(f'User with {product_id} is Not Found in database', status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(self.get_product(product_id), data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

    def delete(self, request, product_id):
        if not self.get_product(product_id):
            return Response(f'User with {product_id} is Not Found in database', status=status.HTTP_404_NOT_FOUND)
        model = self.get_product(product_id)
        model.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)