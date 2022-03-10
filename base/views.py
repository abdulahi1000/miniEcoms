from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from .serializers import *
from django.http import HttpResponse


# Create your views here.
@api_view(['GET'])
def getProducts(request):
    products = Product.objects.all()

    serializer = ProductSerializer(products, many=True)

    return Response(serializer.data)


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
def createProduct(request):
    data = request.data
    user = request.user

    if data:
        product = Product.object.create(
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


@api_view(['DELETE'])
def deleteProduct(request, pk):
    user = request.user
    product = Product.objects.filter(id=pk)

    if product.exists() and user:

        product = product[0]
        product.delete()

        return Response({'details':'Item deleted successfully'})

    else:
        return Response({'details': 'the product is not available'}, status=status.HTTP_204_NO_CONTENT)
   