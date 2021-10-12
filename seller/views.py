from django.conf import settings
from django.http import request
from django.shortcuts import redirect, render
from django.views.generic import ListView
from .models import Seller
from .forms import RegisterForm
from user.models import User
from product.models import Product

image_url = settings.IMAGE_URL

class SellerProductList(ListView):
    model = Product
    template_name = 'seller_product.html'
    context_object_name = 'products'
    paginate_by = 10
        
    def get_queryset(self):
        user_id = self.request.session.get('user')
        if user_id:
            seller_id = Seller.objects.get(user_id=user_id)    
            print(seller_id)
            return Product.objects.filter(seller_id=seller_id)
        return Product.objects.all()

def register(request):
    user_id = request.session.get('user')
    if(request.method == 'POST'):
        seller = Seller()
        seller.user_id = User.objects.get(id=user_id)
        seller.name=request.POST['name']
        seller.address = request.POST['address']
        seller.address_detail = request.POST['address_detail']
        seller.phone_number = request.POST.get('phone_number')
        seller.mobile_number = request.POST.get('mobile_number')
        seller.image =request.FILES.get('image')
        seller.save()
        seller.image = '{}/{}'.format(image_url,seller.image)
        seller.save()
        return redirect('/seller/register')
    else:
        return render(request, 'register_seller.html', {'form':RegisterForm})

def product(request):
    return render(request, 'product.html')