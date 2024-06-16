from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import OrderSummary, Order
from django.core.mail import send_mail
from django.http import HttpResponse
from decouple import config
from .models import Product
from django.db.models import Q
from django.conf import settings
import paypalrestsdk
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.
def index(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'temp_shop_ecommerce/index.html', context=context)

def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            current_site = get_current_site(request)
            """mail_subject = 'User account activation'
            message = render_to_string('temp_shop_ecommerce/registration/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': uid,
                'token': token
            })
            
            send_mail(mail_subject, message, 
                      from_email=config('EMAIL_HOST_USER'), recipient_list=[user.email])"""
            
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            return redirect('index')
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

@login_required
def user_cart(request):
    order_summary = get_object_or_404(OrderSummary, client=request.user.id)

    # Get all Orders associated with this OrderSummary
    orders = Order.objects.filter(order_summary=order_summary)

    # Pass the orders to the template
    return render(request, 'temp_shop_ecommerce/cart.html', {'orders': orders})

@login_required
def create_order(request, product_id):
    if request.method == 'POST':
        orders = Order.objects.filter(order_summary= OrderSummary.objects.get(client=request.user))
        order_summary = OrderSummary.objects.get(client=request.user)
        for order in orders:
            if order.product.id == product_id:
                order_summary.total_price += order.product.price
                order.quantity +=1
                order.save()
                order_summary.save()
                return redirect('index')
        product = get_object_or_404(Product, id=product_id)
        order_summary.total_price += product.price
        order_summary.save()
        Order.objects.create(
            product=product,
            order_summary=order_summary,
            quantity=1
        )
        return redirect('index')
    return redirect('index')

@login_required
def delete_item(request, order_id):
    order = get_object_or_404(Order, id=order_id, order_summary=OrderSummary.objects.get(client=request.user))
    #order_summary = OrderSummary.objects.get(client=request.user)
    #product = get_object_or_404(Product, id=order.product.id)
    #order_summary.total_price -= order.product.price * order.quantity
    #order_summary.save()
    #product.stored_quantity +=order.quantity
    order.delete()
    return redirect('cart')

def search_view(request):
    query = request.GET.get('query', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    
    # Start with all products
    products = Product.objects.all()

    # Apply the name filter if query is provided
    if query:
        products = products.filter(Q(name__istartswith=query))

    # Debug: Print the initial queryset count
    print(f"Initial products count after name filter: {products.count()}")

    # Convert min_price and max_price to floats for comparison, if they are provided and not empty
    try:
        min_price = float(min_price) if min_price else None
        max_price = float(max_price) if max_price else None
    except ValueError:
        # Handle the case where min_price or max_price are not valid numbers
        min_price, max_price = None, None

    # Debug: Print the min_price and max_price values
    print(f"min_price: {min_price}, max_price: {max_price}")

    # Apply price filters
    if min_price is not None and max_price is not None:
        products = products.filter(price__range=(min_price, max_price))
    elif min_price is not None:
        products = products.filter(price__gte=min_price)
    elif max_price is not None:
        products = products.filter(price__lte=max_price)

    # Debug: Print the final queryset count after price filter
    print(f"Final products count after price filter: {products.count()}")

    # If no filters are applied and no products match the query, return an empty queryset
    if not query and min_price is None and max_price is None:
        products = Product.objects.none()

    return render(request, 'temp_shop_ecommerce/search.html', {'products': products})

paypalrestsdk.configure({
    'mode': 'sandbox',  # Change to 'live' for production
    'client_id': 'AaTTmqw77F5AO8wLW-Adqgn7RwApTT-mRDiUhe-7TtiZs0yXzGz8q8nVYT7jUFPp50IiQSo2N06rBL8W',
    'client_secret': 'EJU_p9iBYxx24OHnlU4r-6sEHys5-5BbmTNylzoU0rdOzsNF-B9UUW_sQH3Irz3ajxihgtQU8SQIyJSF'
})

def payment_process(request):
    order = get_object_or_404(OrderSummary, client=request.user)

    payment = paypalrestsdk.Payment({
        'intent': 'sale',
        'payer': {'payment_method': 'paypal'},
        'redirect_urls': {
            'return_url': request.build_absolute_uri(reverse('index')),
            'cancel_url': request.build_absolute_uri(reverse('index')),
        },
        'transactions': [{
            'amount': {'total': str(order.total_price), 'currency': 'PLN'},
            'description': 'Payment for your order',
        }]
    })

    if payment.create():
        for link in payment.links:
            if link.rel == 'approval_url':
                approval_url = link.href
                return redirect(approval_url)
    else:
        return redirect('index')
