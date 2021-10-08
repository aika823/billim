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
    path('', views.login),

    path('login/', views.login),    
    path('login/<str:type>/', views.login_social, name="custom_login" ),

    path('register/', views.create),
    path('logout/', views.logout),

    path('callback/google/login', views.callback_google, name="custom_login" ),
    path('callback/kakao/', views.callback_kakao),
    path('callback/naver/', views.callback_naver),
]