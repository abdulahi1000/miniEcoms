from django.urls import path

from . import views

urlpatterns = [
    path('products/', views.getProducts, name='products'),
    path('product/<str:pk>/', views.getProduct, name='product'),
    path('product/create/', views.createProduct, name='product-create'),
    path('product/delete/<str:pk>/', views.deleteProduct, name='product-delete'),
]
