import json
from os import access
import requests
import base64

from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.conf import settings

from .forms import RegisterForm
from .forms import LoginForm, RegisterForm
from .models import User
from .forms import RegisterForm
from user.decorators import admin_required

client_id_naver = 'WO73y3DTPypJ9B7qq56N'
client_id_kakao = 'afa386bd37692148a6c914da561c8458'
billim_url = settings.BILLIM_URL
image_url = settings.IMAGE_URL

# def home(request):
#     return render(request, 'home.html')

def index(request):
    return render(request, 'index.html', { 'email': request.session.get('user') })

def logout(request):
    if 'user' in request.session:
        del(request.session['user'])
    return redirect('/')

def callback_google123(request):
    print("callback_google123 function")
    url ='https://accounts.google.com/o/oauth2/auth/identifier'
    redirect_uri = 'http://localhost:8000/user/callback/google/login'
    google_auth_api = "https://accounts.google.com/o/oauth2/v2/auth"
    client_id = '1094555666329-b76moi8dkckmoe3vc9kb2qhf60r8t563.apps.googleusercontent.com'
    scope = "https://www.googleapis.com/auth/userinfo.email "+"https://www.googleapis.com/auth/userinfo.profile"

    params = {
        'client_id':client_id,
        'redirect_uri': redirect_uri,
        'scope':scope,
        'response_type':'code',
        'state':'LW3T3VwQn30o',
        'flowName':'GeneralOAuthFlow'
    }
    
    response = redirect( f"{google_auth_api}?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope={scope}" ) 
    return response

    
def callback_google(request):
    # 인증 요청
    code = request.GET.get('code')    
    url_auth = 'https://oauth2.googleapis.com/token'
    client_id = '1094555666329-b76moi8dkckmoe3vc9kb2qhf60r8t563.apps.googleusercontent.com'
    client_secret = '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'
    scope = "https://www.googleapis.com/auth/userinfo.profile"
    data = {
        "grant_type":'authorization_code',
        'client_id':client_id,
        'client_secret':client_secret,
        'redirect_uri':'http://localhost:8000/user/callback/google/login',
        'code':str(code),
        'scope':scope,
    }
    response = requests.request("POST",url_auth,data=data).json()
    access_token = response['access_token'] 
    
    # 유저 정보 조회
    url_user_info = "https://www.googleapis.com/oauth2/v3/userinfo"
    user_info = requests.request("GET", url_user_info, params={ 'access_token': access_token }).json()
    
    # url_user_info = "https://www.googleapis.com/oauth2/v3/tokeninfo"
    # user_info = requests.request("GET", url_user_info, params={ 'id_token': response['id_token'] }).json()

    # url_user_info = "https://www.googleapis.com/userinfo/v2/me"
    # user_info = requests.request("GET", url_user_info, params={ 'access_token': access_token }).json()

    print(user_info)
    return render(request, 'home.html')


def callback_naver(request):
    # 인증 요청
    code = request.GET.get('code')    
    url_auth = 'https://nid.naver.com/oauth2.0/token/'
    redirect_uri= billim_url+'/user/callback/naver'
    client_id ="WO73y3DTPypJ9B7qq56N"
    client_secret = "SOUKrwtgel"
    state = "REWERWERTATE"
    clientConnect = client_id + ":" + client_secret
    clidst_base64 = base64.b64encode(bytes(clientConnect, "utf8")).decode()
    headers = {"Authorization": "Basic "+clidst_base64}
    data = {
        "grant_type":'authorization_code',
        'client_id':client_id,
        'client_secret':client_secret,
        'redirect_uri':redirect_uri,
        'code':code,
        'state':state,
    }
    response = requests.request("POST",url_auth,data=data,headers=headers).json()
    access_token = response['access_token']

    # 유저 정보 조회
    url_user_info = "https://openapi.naver.com/v1/nid/me"
    user_header = {'Authorization':"Bearer " + access_token}
    user_info = requests.request("POST", url_user_info, headers=user_header).json()
    username = user_info['response']['name']
    email = user_info['response']['email']

    # DB에 추가
    user = User(
                username=username,
                email=email,
                password=None,
                social_login='naver'
            )
    user.save()
    # 네이버 로그인 성공 
    request.session['user'] = user.id
    return render(request, 'home.html', {'test': user_info, 'code':code, 'access_token':access_token})

def callback_kakao(request):
    # 인증 요청
    url_auth = 'https://kauth.kakao.com/oauth/token'  
    code = request.GET.get('code')
    data = {
        'grant_type' : 'authorization_code',
        'client_id' : '8697dec0f53599c5d7f2502389d16f72',
        'redirect_uri' : billim_url+'/user/callback/kakao',
        'code' : code,
    }
    response = requests.request("POST", url_auth, data=data, verify=False).json()
    access_token = response['access_token']
    
    # 유저 정보 조회
    url_user_info = 'https://kapi.kakao.com/v2/user/me'
    my_token = 'Bearer '+str(access_token)
    header = {'Authorization': my_token}
    user_info = requests.request("POST", url_user_info, headers=header, verify=False).json()
    username = user_info['kakao_account']['profile']['nickname']
    email = user_info['kakao_account']['email']
    
    # DB에 추가
    user = User(
                username=username,
                email=email,
                password=None,
                social_login='kakao'
            )
    user.save()
    
    # 카카오 로그인 성공 
    request.session['user'] = user.id
    return render(request, 'home.html', {'test': user_info, 'code':code, 'access_token':access_token})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            request.session['user'] = form.user_id
            # username = User.objects.values('username')
            username = User.objects.filter(id=form.user_id).values('username')[0]['username']
            image_src = str(User.objects.filter(id=form.user_id).values('image')[0]['image'])
            # username = User.objects

            return render(request, 'home.html', {'username':username, 'image_src':image_src})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form, 'url':billim_url})

def create(request):
    if(request.method == 'POST'):
        user = User()
        user.username=request.POST['username']
        user.email=request.POST['email']
        user.password=make_password(request.POST['password'])
        user.image = request.FILES.get('image')
        user.save()
        user.image = '{}{}'.format(image_url,user.image) # Save full url in database
        user.save()
        return redirect('/user/login')
    else:
        return render(request, 'register.html', {'form':RegisterForm})

class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/'
    def form_valid(self, form):
        self.request.session['user'] = form.data.get('email')
        return super().form_valid(form)