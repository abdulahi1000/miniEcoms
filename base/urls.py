from django.urls import path

from . import views

urlpatterns = [
    path('products/', views.getProducts, name='products'),
    path('products-category/', views.getProductsByCategory, name='products-category'),
    path('product/create/', views.createProduct, name='product-create'),
    path('product/order/', views.orderProduct, name='product-order'),

    path('product/<str:pk>/', views.getProduct, name='product'),
    path('product/update/<str:pk>/', views.updateProduct, name='product-update'),
    path('product/delete/<str:pk>/', views.deleteProduct, name='product-delete'),

    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/', views.registerUser, name='register'),
    path('register/admin/', views.registerAdminUser, name='register-admin'),
]
