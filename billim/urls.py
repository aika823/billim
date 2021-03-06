import datetime
from datetime import date
from django.conf import settings
from django.contrib import admin
from django.conf import settings  # new
from django.urls import path, include  # new

from django.template.response import TemplateResponse
from django.urls import path, include, re_path
from django.conf.urls.static import static
from user.views import index, logout, LoginView
from product.views import (ProductListAPI, ProductDetailAPI)
from order.views import OrderCreate, OrderList
from django.views.generic import TemplateView
from order.models import Order
from .functions import get_exchange

orig_index = admin.site.index

def index(request, extra_context=None):
    base_date = datetime.datetime.now() - datetime.timedelta(days=7)
    order_data = {}
    for i in range(7):
        target_dttm = base_date + datetime.timedelta(days=i)
        date_key = target_dttm.strftime('%Y-%m-%d')
        target_date = datetime.date(target_dttm.year, target_dttm.month, target_dttm.day)
        order_cnt = Order.objects.filter(register_date__date=target_date).count()
        order_data[date_key] = order_cnt

    extra_context = {
        'orders': order_data,
        'exchange': get_exchange()
    }

    return orig_index(request, extra_context)

admin.site.index = index


urlpatterns = [
    re_path(r'^admin/manual/$',
        TemplateView.as_view(template_name='admin/manual.html',
        extra_context={'title': '매뉴얼', 'site_title': '패스트캠퍼스', 'site_header': '패스트캠퍼스'})
    ),
    path('', include('user.urls')),
    path('admin/', admin.site.urls),

    path('api/', include('rest_framework.urls')),
    path('api/product/', ProductListAPI.as_view()),
    path('api/product/<int:pk>/', ProductDetailAPI.as_view()),

    path('baton/',      include('baton.urls')),
    path('board/',      include('board.urls')),
    path('product/',    include('product.urls')),
    path('order/',      include('order.urls')),
    path('seller/',     include('seller.urls')),
    path('user/',       include('user.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
