from django import VERSION
from django.http import request
from django.shortcuts import render, redirect
from django.views.generic import DetailView
from django.views.generic.edit import FormView
from django.contrib.auth.hashers import make_password
from django.views.generic.list import ListView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password

from .forms import LoginForm
from .models import User

import requests
import time

from rest_framework import status
from rest_framework.response import Response

def home(request):
    return render(request, 'home.html')

def index(request):
    return render(request, 'index.html', { 'email': request.session.get('user') })

def logout(request):
    if 'user' in request.session:
        del(request.session['user'])
    return redirect('/')

def callback(request):
    url = 'https://kauth.kakao.com/oauth/token'
    code = request.GET.get('code')
    data = {
        'grant_type' : 'authorization_code',
        'client_id' : '8697dec0f53599c5d7f2502389d16f72',
        'redirect_uri' : 'http://localhost:8000/user/callback/kakao',
        'code' : code,
    }
    response = requests.request("POST", url, data=data, verify=False)
    access_token = response.json()['access_token']

    url2 = 'https://kapi.kakao.com/v2/user/me'
    my_token = 'Bearer '+str(access_token)
    header = {
        'Authorization': my_token
    }
    response2 = requests.request("POST", url2, headers=header, verify=False)
    
    password = 'kakao'
    username = response2.json()['kakao_account']['profile']['nickname']
    email = response2.json()['kakao_account']['email']



    user = User(
                username=username,
                email=email,
                password=make_password(password)
            )

    user.save()

    
    return render(request, 'callback.html', {'test': response2.json(), 'code':code, 'access_token':access_token})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            request.session['user'] = form.user_id
            return redirect('/')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    elif request.method == 'POST':
        username = request.POST.get('username', None)
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        re_password = request.POST.get('re-password', None)

        res_data = {}

        if not (username and email and password and re_password):
            res_data['error'] = '모든 값을 입력해야합니다.'
        elif password != re_password:
            res_data['error'] = '비밀번호가 다릅니다.'
        else:
            user = User(
                username=username,
                email=email,
                password=make_password(password)
            )

            user.save()

        return render(request, 'register.html', res_data)

# class RegisterView(FormView):
#     template_name = 'register.html'
#     form_class = RegisterForm
#     success_url = '/'
#     def form_valid(self, form):
#         user = User(
#             email=form.data.get('email'),   
#             password=make_password(form.data.get('password')),
#             level='user'
#         )
#         user.save()
#         return super().form_valid(form)


class LoginView(FormView):
    # template_name = 'login.html'
    template_name = 'login_form.html'
    form_class = LoginForm
    success_url = '/'
    def form_valid(self, form):
        self.request.session['user'] = form.data.get('email')
        return super().form_valid(form)