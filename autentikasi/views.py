from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.http.request import HttpRequest
from django.http.response import HttpResponseRedirect

from ki_tugas1.views import Views
from .models import User
from .forms import FormLogin, FormRegister

class Login(Views):

    def get(self, request: HttpRequest, *args, **kwargs):
        return render(request, 'login.html')
    
    def post(self, request: HttpRequest, *args, **kwargs):
        form = FormLogin(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is None:
                return HttpResponseRedirect('/auth/login/')
            login(request, user)
            return HttpResponseRedirect('/info/user/')
                
            
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class Register(Views):

    def get(self, request: HttpRequest, *args, **kwargs):
        return render(request, 'register.html')
    
    def post(self, request: HttpRequest, *args, **kwargs):
        form = FormRegister(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user_lain = User.objects.filter(username=username).first()
            
            if user_lain is not None:
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            
            User.objects.create_user(username=username, password=password)
            return HttpResponseRedirect("/auth/login/")
            
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))