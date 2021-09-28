from django.http import request
from django.shortcuts import render, redirect
from django.views.generic import DetailView
from django.views.generic.edit import FormView
from django.contrib.auth.hashers import make_password
from django.views.generic.list import ListView
from .forms import RegisterForm, LoginForm
from .models import User


# Create your views here.

def index(request):
    return render(request, 'index.html', { 'email': request.session.get('user') })

def logout(request):
    if 'user' in request.session:
        del(request.session['user'])
        
    return redirect('/')

def callback(request):
    print("###################")
    for value in request.__dict__:
        print(value)
    
    
    return render(request, 'callback.html')





class RegisterView(FormView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = '/'

    def form_valid(self, form):
        user = User(
            email=form.data.get('email'),   
            password=make_password(form.data.get('password')),
            level='user'
        )
        user.save()

        return super().form_valid(form)


class LoginView(FormView):
    # template_name = 'login.html'
    template_name = 'login_form.html'
    form_class = LoginForm
    success_url = '/'

    def form_valid(self, form):
        self.request.session['user'] = form.data.get('email')

        return super().form_valid(form)