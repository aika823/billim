import json
from os import access
from django.db.models.expressions import F, Case, When
from django.db.models.fields import CharField
from django.db.models.query_utils import Q, FilteredRelation
import requests
import base64

from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.conf import settings
from requests.sessions import session
from rest_framework import viewsets

from product.models import Product, ProductImage
from seller.models import Seller
from user.serializer import UserSerializer

from .forms import RegisterForm
from .forms import LoginForm, RegisterForm
from .models import User
from .forms import RegisterForm
from user.decorators import admin_required

client_id_naver = settings.NAVER_CLIENT_ID
client_id_kakao = settings.KAKAO_CLIENT_ID
billim_url = settings.BILLIM_URL
image_url = settings.IMAGE_URL

def index(request):
    return render(request, 'index.html', { 'email': request.session.get('user') })

def logout(request):
    if 'user' in request.session:
        del(request.session['user'])
    return redirect('/')

def login_social(request, type):
    url_auth = {
        'naver' : "https://nid.naver.com/oauth2.0/authorize",
        'kakao' : "https://kauth.kakao.com/oauth/authorize",
        'google': "https://accounts.google.com/o/oauth2/v2/auth"
    }
    response_type = {
        'naver' : 'code',
        'kakao' : 'code',
        'google': 'code'
    }
    client_id = {
        'naver' : 'WO73y3DTPypJ9B7qq56N',
        'kakao' : 'afa386bd37692148a6c914da561c8458',
        'google': '1094555666329-b76moi8dkckmoe3vc9kb2qhf60r8t563.apps.googleusercontent.com'
    }
    redirect_uri = {
        'naver' : billim_url+'/user/callback/naver/',
        'kakao' : billim_url+'/user/callback/kakao',
        'google': billim_url+'/user/callback/google'
    }
    scope={
        'naver' : None,
        'kakao' : None,
        'google': "https://www.googleapis.com/auth/userinfo.email "+"https://www.googleapis.com/auth/userinfo.profile"
    }
    state = {
        'naver' : '7a74649e-d714-438f-a3fc-991c8b6f4bc7',
        'kakao' : None,
        'google': None
    }
    str_auth = f"{url_auth[type]}?response_type={response_type[type]}&client_id={client_id[type]}&redirect_uri={redirect_uri[type]}&state={state[type]}"
    if scope[type]: str_auth += "&scope={}".format(scope[type])
    response = redirect(str_auth)
    return response
    
def callback_social(request, type):    
    
    # ????????? ????????? ?????? ?????? ?????? ??????
    code = request.GET.get('code')    
    url_auth = {
        'google': 'https://oauth2.googleapis.com/token',
        'naver' : 'https://nid.naver.com/oauth2.0/token',
        'kakao' : 'https://kauth.kakao.com/oauth/token'  
    }
    client_id={
        'google': '1094555666329-b76moi8dkckmoe3vc9kb2qhf60r8t563.apps.googleusercontent.com',
        'naver' : "WO73y3DTPypJ9B7qq56N",
        'kakao' : '8697dec0f53599c5d7f2502389d16f72'
    }
    client_secret={
        'google': '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', #??????
        'naver' : "SOUKrwtgel", #?????????
    }
    scope={
        'google': "https://www.googleapis.com/auth/userinfo.profile"
    }
    state={
        'naver' : "REWERWERTATE"
    }
    redirect_uri = {
        'google': billim_url+'/user/callback/google',
        'naver' : billim_url+'/user/callback/naver',
        'kakao' : billim_url+'/user/callback/kakao',
    }
    if type == 'naver':
        clientConnect = client_id[type] + ":" + client_secret[type]
        clidst_base64 = base64.b64encode(bytes(clientConnect, "utf8")).decode()
        headers = {"Authorization": "Basic "+clidst_base64}
    else:
        headers = None
        
    data = {
        "grant_type":'authorization_code',
        'client_id':client_id[type],
        'redirect_uri':redirect_uri[type],
        'code':code,
    }
    if type in client_secret:
        data['client_secret'] = client_secret[type]
    if type in scope:
         data['scope'] = scope[type] 
    if type in state:
        data['state'] = state[type] 
    response = requests.request("POST", url_auth[type], data=data,headers=headers).json()
    
    # ????????? ?????? ??????
    access_token = response['access_token'] 

    # ????????? ????????? ?????? ?????? ?????? ??????
    if type == 'google':
        url_user_info = "https://www.googleapis.com/oauth2/v3/userinfo"
        user_response = requests.request("POST", url_user_info, params={'access_token': access_token }).json()
        username = user_response['email']
        email = user_response['email']
        social_id = user_response['sub']

    elif type == 'naver':
        url_user_info = "https://openapi.naver.com/v1/nid/me"
        header = {'Authorization':"Bearer " + access_token}
        user_response = requests.request("POST", url_user_info, headers=header).json()
        username = user_response['response']['name']
        email = user_response['response']['email']
        social_id = user_response['response']['id']
    
    elif type == 'kakao':
        url_user_info = "https://kapi.kakao.com/v2/user/me"
        header = {'Authorization':"Bearer " + access_token}
        user_response = requests.request("POST", url_user_info, headers=header, verify=False).json()
        username = user_response['kakao_account']['profile']['nickname'] #?????????
        email = user_response['kakao_account']['email']
        social_id = user_response['id']

    # ?????? ??????
    user_info = {
        'username': username,
        'email': email,
        'social_id': social_id
    }
    
    # DB?????? ???????????? ?????? ??? ?????? ?????? ?????? 
    user_in_db = User.objects.get(social_id=social_id)
    if user_in_db:
        user = user_in_db
    else:
        user = User(
                    username=username,
                    email=email,
                    password=None,
                    social_login=type,
                    social_id = social_id
                )
        user.save()

    # ?????? ????????? ??? ??????????????? ??????
    request.session['user'] = user.id

    
    # request.session['user_obj'] = user 
    # ?????? ??????????????? ?????????...



    # return render(request, 'home.html', {'test': user_info})
    return redirect('/')

def login(request):
    # ????????? ??? ?????? ???
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            request.session['user'] = form.user_id
            username = User.objects.filter(id=form.user_id).values('username')[0]['username']
            image_src = str(User.objects.filter(id=form.user_id).values('image')[0]['image'])
            return render(request, 'home.html', {'username':username, 'image_src':image_src})
    else:
        # ????????? ??? ??????
        if 'user' in request.session: 
            user = User.objects.get(id=request.session['user'])
            try:
                seller = Seller.objects.get(user_id=user)
            except Seller.DoesNotExist:
                seller = None
            form = None
        # ????????? ??? ??? ??????
        else: 
            user = None
            seller = None
            form = LoginForm()
        
        products = Product.objects.annotate(
            image = Case(
                When(productimage__thumbnail=True, then=F('productimage__image')),
                output_field=CharField()
            )
        ).filter(image__isnull = False)
        

    return render(request, 'login.html', {
        'form': form, 
        'user':user, 
        'seller': seller,
        'products':products, 
    })

class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/'
    def form_valid(self, form):
        self.request.session['user'] = form.data.get('email')
        return super().form_valid(form)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

