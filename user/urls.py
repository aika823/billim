from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register),
    path('login/', views.login),
    path('logout/', views.logout),
    path('callback/kakao', views.callback_kakao),
    path('callback/naver', views.callback_naver),
]