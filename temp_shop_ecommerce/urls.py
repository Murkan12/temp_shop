from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('cart/', views.user_cart, name='cart'),
    path('create_order/<int:product_id>/', views.create_order, name='create_order'),
    path('delete_item/<int:order_id>/', views.delete_item, name='delete_item'),
    
    # Test
    #path('send-test-email/', views.send_test_email, name="test_mail")
]