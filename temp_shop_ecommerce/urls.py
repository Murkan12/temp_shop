from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    
    path('register/', views.user_register, name='register'),
    path('email-confirmation-sent/', views.email_confirmation_sent, name="email_confirmation_sent"),
    path("activate/<uidb64>/<token>/", views.activate_user, name="activate"),
    
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('cart/', views.user_cart, name='cart'),
    path('create_order/<int:product_id>/', views.create_order, name='create_order'),
    path('delete_item/<int:order_id>/', views.delete_item, name='delete_item'),
    path('delete_item/<int:order_id>/', views.delete_item, name='delete_item'),
    path('search/', views.search_view, name='search'),
    path('payment/', views.payment_process, name='payment_process'),
    path('filter/', views.price_filter, name='filter'),
    
    # Test
    #path('send-test-email/', views.send_test_email, name="test_mail")
]