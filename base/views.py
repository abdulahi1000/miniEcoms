from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .serializers import *

# for simple jwt
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


# Create your views here.
@api_view(['GET'])
def getProducts(request):
    products = Product.objects.all()

    serializer = ProductSerializer(products, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def getProductsByCategory(request):
    data = request.data
    products = Product.objects.filter(category=data['category'])
    if products:
        serializer = ProductSerializer(products, many=True)

        return Response(serializer.data)
    else:
        return Response({'details':'No product for the category'}, status=status.HTTP_404_NOT_FOUND) 

@api_view(['GET'])
def getProduct(request, pk):
    product = Product.objects.filter(id=pk)

    if product.exists():
        product = product[0]
        serializer = ProductSerializer(product, many=False)

        return Response(serializer.data)
    
    else:
        return Response({'details':'the product is not available'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def createProduct(request):
    data = request.data
    user = request.user

    if user.is_staff == True:

        if data:
            product = Product.objects.create(
                user=user,
                title=data['title'],
                category=data['category'],
                description=data['description'],
                price=data['price'],
                countInStock=data['countInStock'],

            )
            serializer = ProductSerializer(product, many=False)
            return Response(serializer.data)
        else:
            return Response({'details': 'please provide required data'}, status=status.HTTP_204_NO_CONTENT)
    else:
        return Response({'details':'you are not authorized'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateProduct(request, pk):
    data = request.data
    user = request.user

    product = Product.objects.filter(id=pk)
    if product.exists() and data:
        if user.is_staff == True:
            product = product[0]
            product.title = data['title']
            product.category = data['category']
            product.description = data['description']
            product.price = int(data['price'])
            product.countInStock = int(data['countInStock'])

            product.save()
            serializer = ProductSerializer(product, many=False)
            return Response(serializer.data)

        else:
            return Response({'details':'you are not authorized'}, status=status.HTTP_401_UNAUTHORIZED)

    else:
        return Response({'details': 'the product is not available'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteProduct(request, pk):
    user = request.user
    product = Product.objects.filter(id=pk)

    if user.is_staff == True:

        if product.exists():

            product = product[0]
            product.delete()

            return Response({'details':'Item deleted successfully'})

        else:
            return Response({'details': 'the product is not available'}, status=status.HTTP_204_NO_CONTENT)
    else:
        return Response({'details': 'you are not authorized'}, status=status.HTTP_401_UNAUTHORIZED)



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data

        for k, v in serializer.items():
            data[k] = v

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['POST'])
@permission_classes([IsAdminUser])
def registerUser(request):

    data = request.data
    user = request.user
    if user.is_staff == True:
        try:
            user = User.objects.create_user(
                first_name=data['first_name'],
                last_name=data['last_name'],
                username=data['email'],
                email=data['email'],
                password=data['password']
            )

            serializer = UserSerializerWithToken(user, many=False)

            return Response(serializer.data)
        except:
            massage = {'detail': 'user with this email already exists'}
            return Response(massage, status=status.HTTP_400_BAD_REQUEST)
    
    else:
        return Response({'details': 'you are not authorized'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def registerAdminUser(request):

    data = request.data
    user = request.user
    if user.is_staff == True:
        try:
            user = User.objects.create_user(
                first_name=data['first_name'],
                last_name=data['last_name'],
                username=data['email'],
                email=data['email'],
                is_staff= True,
                password=data['password']
            )

            serializer = UserSerializerWithToken(user, many=False)

            return Response(serializer.data)
        except:
            massage = {'detail': 'user with this email already exists'}
            return Response(massage, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response({'details': 'you are not authorized'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def orderProduct(request):
    user = request.user
    data = request.data

    if user and data:
        product = Product.objects.filter(id=data['pk'])
        if product.exists():
            product = product[0]
            if int(data['amount']) >= product.price:
                if int(data['quantity']) <= product.countInStock:
                    product.countInStock -=int(data['quantity'])
                    product.save()
                    return Response({'details':'Order placed successfully'}, status=status.HTTP_201_CREATED)
                else:
                    return Response({'details': 'product quantity is more than what is available'}, status=status.HTTP_204_NO_CONTENT)

                pass
            else:
                return Response({'details':'no sufficiant amount'}, status=status.HTTP_406_NOT_ACCEPTABLE)

            pass
        else:
            return Response({'details': 'the product is not available'}, status=status.HTTP_204_NO_CONTENT)

    pass
