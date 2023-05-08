from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
# from django.views.generic import View



# Error 처리 view (DEBUG = False일 경우만 동작)
def error_404_view(request, exception):
    return HttpResponseNotFound("The page is not found")

def index(request):
    return render(request, 'main.html')


def login_view(request):
    if(request.method == 'POST'):
        print('request', request)
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        
        if(user is not None):
            login(request, user)
            return redirect('index')
    
        else:
            return render(request, 'registration/login.html' )
    
    elif(request.method == 'GET'):
        return render(request, 'registration/login.html')

def logout_view(request):
    if(request.method == 'GET'):
        logout(request)
        return redirect('index')
    else:
        return render(request, 'registration/logged_out.html')

