from django.conf import settings
from django.forms.fields import ImageField
from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator
from order.models import Order
from rest_framework import generics
from rest_framework import mixins

from .models import Category, Product, ProductCategory, ProductImage, Qna, Subcategory
from .forms import AnswerForm, ProductRegisterForm, QuestionForm
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
    images = ProductImage.objects.filter(product_id=product_id)
    product_category = product.category_id
    context = {
        'product': product,
        'images': images,
        'form': OrderForm,
        'question_form': QuestionForm,
        'answer_form': AnswerForm,
        'category': product_category.category_id,
        'subcategory': product_category.subcategory_id,
        'qna_list': Qna.objects.filter(product_id=product_id)
    }
    return render(request, 'product_detail.html', context)


def create(request):

    # 로그인 된 유저의 셀러 등록여부 확인
    user_id = request.session.get('user')
    try:
        seller = Seller.objects.get(user_id=user_id)
    except Seller.DoesNotExist:
        seller = None

    # 셀러 상품 등록 로직
    if (request.method == 'POST') & (seller is not None):

        # 상품 기본정보 저장
        product = Product() 
        product.name = request.POST['name']
        product.price = request.POST['price']
        product.description = request.POST['description']
        product.stock = request.POST['stock']
        product.seller_id = seller
        
        # 카테고리 정보 저장
        product_category = ProductCategory()
        product_category.category_id_id = request.POST['category']
        product_category.subcategory_id_id = request.POST['subcategory']
        product_category.save()
        product.category_id = product_category
        product.save()

        # 썸네일 이미지 저장
        thumbnail_image = ProductImage()
        thumbnail_image.product_id = product
        thumbnail_image.image = request.FILES.get('thumbnail_image')
        thumbnail_image.thumbnail = True
        thumbnail_image.save()
        thumbnail_image.image = '{}/{}'.format(image_url, thumbnail_image.image)
        thumbnail_image.save()

        # 상품 이미지 저장
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
            return render(request, 'product_register.html', {'product_form': ProductRegisterForm})
        else:
            return render(request, 'product_register.html', {'form': None})


def add_qna(request):
    user_id = request.session.get('user')
    if (request.method == 'POST'):
        qna_id = request.POST.get('qna_id')
        # 답변    
        if qna_id:
            qna = Qna.objects.get(id=qna_id)
            qna.answer = request.POST.get('answer')
        # 질문
        else:
            qna = Qna()
            qna.question = request.POST.get('question')
            qna.user_id = user_id
            qna.product_id = request.POST.get('product_id')
        
        qna.save()
    return redirect(request.META['HTTP_REFERER'])
        