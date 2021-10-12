from django.urls.conf import path
from .views import OrderList, OrderCreate

urlpatterns = [
    path('order/', OrderList.as_view()),
    path('order/create/', OrderCreate.as_view()),
]