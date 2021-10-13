from django.urls.conf import path
from .views import ProductList, add_qna, bookmark, product_detail, create

urlpatterns = [
    path('', ProductList.as_view()),
    path('<int:product_id>/', product_detail),
    path('create/', create),
    path('qna/', add_qna),
    path('<int:product_id>/bookmark/', bookmark)
    # path('product/<int:pk>/', ProductDetail.as_view()),
    # path('product/create/', ProductCreate.as_view()),
]