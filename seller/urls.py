from django.urls import path
from . import views
from product.views import ProductDetail, ProductList

urlpatterns = [
    path('register', views.register),
    path('product/', views.SellerProductList.as_view()),
    path('product/<int:pk>/', ProductDetail.as_view()),
]