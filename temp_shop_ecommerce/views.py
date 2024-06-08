from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
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
            user = form.save()
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            current_site = get_current_site(request)
            mail_subject = 'User account activation'
            message = render_to_string('temp_shop_ecommerce/registration/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': uid,
                'token': token
            })
            
            send_mail(mail_subject, message, 
                      from_email=config('EMAIL_HOST_USER'), recipient_list=[user.email])
            
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            return redirect('email_confirmation_sent')
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

def email_confirmation_sent(request):
    return render(request, 'temp_shop_ecommerce/registration/email_confirmation_sent.html')

def activate_user(request, uidb64, token):
    try:
        User = get_user_model()
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')
    else:
        return render(request, 'registration/activation_invalid.html')

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