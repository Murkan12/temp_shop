from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from .forms import UserRegisterForm
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponse
from decouple import config

# Create your views here.
def index(request):
    return render(request, 'temp_shop_ecommerce/index.html')

def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            
            
            send_mail('User account activation', f'Hi {user.username}!\nPlease click this link to finalize the account creation process: f{}')
            
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'temp_shop_ecommerce/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f'You are now logged in as {username}.')
                return redirect('index')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'temp_shop_ecommerce/login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.info(request, 'You have successfully logged out.')
    return redirect('index')

# TEST FUNCTION DO NOT IMPLEMENT
def send_test_email(request):
    try:
        send_mail('Test Mail', 'This is test mail sent from Django.', from_email=config('EMAIL_HOST_USER'),
              recipient_list=['loud3ds@gmail.com'], fail_silently=False)
    except Exception as e:
        return HttpResponse(f'Error occured: {e}')
    
    return HttpResponse('Test email sent successfully.')