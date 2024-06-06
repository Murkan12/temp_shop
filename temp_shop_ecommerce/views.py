from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import OrderSummary, Order
from django.core.mail import send_mail
from django.http import HttpResponse
from decouple import config
from .models import Product

# Create your views here.
def index(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'temp_shop_ecommerce/index.html', context=context)

def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=True)
            user.is_active = False
            order_summary = OrderSummary.objects.create(
                client=user,
                total_price=0,
                address='Address',
                city='City',
                phone_number='Phone Number'
            )
            
            #send_mail('User account activation', f'Hi {user.username}!\nPlease click this link to finalize the account creation process: f{}')
            
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

def user_cart(request):
    order_summary = get_object_or_404(OrderSummary, client=request.user.id)

    # Get all Orders associated with this OrderSummary
    orders = Order.objects.filter(order_summary=order_summary)

    # Pass the orders to the template
    return render(request, 'temp_shop_ecommerce/cart.html', {'orders': orders})

@login_required
def create_order(request, product_id):
    if request.method == 'POST':
        orders = Order.objects.all()
        for order in orders:
            if order.product.id == product_id:
                order.quantity +=1
                order.save()
                return redirect('index')
        product = get_object_or_404(Product, id=product_id)
        order_summary = OrderSummary.objects.get(client=request.user)
        Order.objects.create(
            product=product,
            order_summary=order_summary,
            quantity=1
        )
        return redirect('index')
    return redirect('index')

def delete_item(request, order_id):
    order = get_object_or_404(Order, id=order_id, order_summary = OrderSummary.objects.get(client=request.user))
    product = get_object_or_404(Product, id=order.product.id)
    product.stored_quantity +=order.quantity
    order.delete()
    return redirect('cart')

# TEST FUNCTION DO NOT IMPLEMENT
"""def send_test_email(request):
    try:
        send_mail('Test Mail', 'This is test mail sent from Django.', from_email=config('EMAIL_HOST_USER'),
              recipient_list=['loud3ds@gmail.com'], fail_silently=False)
    except Exception as e:
        return HttpResponse(f'Error occured: {e}')
    
    return HttpResponse('Test email sent successfully.')"""