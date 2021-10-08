from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from . import views
from rest_framework.routers import SimpleRouter

from allauth.account.views import LoginView, SignupView 
from django.urls import path, include  # new



urlpatterns = [
    url('callback/google/', views.callback_google, name="custom_login" ),
    url('callback/google123/', views.callback_google123, name="custom_login" ),

    url('callback/google/login', views.callback_google, name="custom_login" ),

    # url('callback/google/', SignupView.as_view(), name="custom_singup" ),
    # url('callback/google/auth', views.callback_google, name="custom_singup" ),
    
    path('', views.login),
    path('register/', views.create),
    path('login/', views.login),
    path('logout/', views.logout),
    path('callback/kakao/', views.callback_kakao),
    path('callback/naver/', views.callback_naver),
]