from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from . import views
from rest_framework.routers import SimpleRouter


# router = SimpleRouter()
# router.register('register', views.RegisterView)
# urlpatterns = router.urls


urlpatterns = [
    path('register/', views.create),
    # path('register/', views.RegisterView.as_view()),
    path('login/', views.login),
    path('logout/', views.logout),
    path('callback/kakao/', views.callback_kakao),
    path('callback/naver/', views.callback_naver),
]





