from django.conf import settings
from django.forms.fields import ImageField
from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator
from order.models import Order
from rest_framework import generics
from rest_framework import mixins

from .models import Product, ProductImage
from .forms import RegisterForm
from .serializers import ProductSerializer

from user.models import User
from seller.models import Seller
from order.forms import RegisterForm as OrderForm

image_url = settings.IMAGE_URL


class ProductListAPI(generics.GenericAPIView, mixins.ListModelMixin):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.all().order_by('id')

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ProductDetailAPI(generics.GenericAPIView, mixins.RetrieveModelMixin):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.all().order_by('id')

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class ProductList(ListView):
    model = Product
    template_name = 'product.html'
    context_object_name = 'products'
    paginate_by = 10


class ProductDetail(DetailView):
    template_name = 'product_detail.html'
    queryset = Product.objects.all()
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = OrderForm(self.request)
        return context

def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    images = ProductImage.objects.filter(product_id=product)
    form = OrderForm
    return render(request, 'product_detail.html', 
        {
            'product': product,
            'images': images,
            'form': form
        }
    )




def create(request):

    # 로그인 된 유저의 셀러 등록여부 확인
    user_id = request.session.get('user')
    try:
        seller = Seller.objects.get(user_id=user_id)
    except Seller.DoesNotExist:
        seller = None

    # 셀러 상품 등록 로직
    if (request.method == 'POST') & (seller is not None):

        product = Product()
        product.name = request.POST['name']
        product.price = request.POST['price']
        product.description = request.POST['description']
        product.stock = request.POST['stock']
        product.seller_id = seller
        product.image = request.FILES.get('image')
        product.save()

        for img in request.FILES.getlist('images'):
            product_image = ProductImage()
            product_image.product_id = product  
            product_image.image = img
            product_image.save()
            product_image.image = '{}/{}'.format(image_url, product_image.image)    
            product_image.save()
        
        return redirect('/product/'+str(product.id))

    # 셀러 상품 등록 페이지
    else:
        if seller:
            return render(request, 'product_register.html', {'form': RegisterForm})
        else:
            return render(request, 'product_register.html', {'form': None})
