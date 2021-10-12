from django.urls.conf import path
from .views import ProductList, product_detail, create

urlpatterns = [
    path('', ProductList.as_view()),
    path('<int:product_id>/', product_detail),
    path('create/', create),
    # path('product/<int:pk>/', ProductDetail.as_view()),
    # path('product/create/', ProductCreate.as_view()),
]