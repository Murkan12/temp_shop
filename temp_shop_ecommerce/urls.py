from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    
    path('register/', views.user_register, name='register'),
    path('email-confirmation-sent/', views.email_confirmation_sent, name="email_confirmation_sent"),
    path("activate/<uidb64>/<token>/", views.activate_user, name="activate"),
    
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # Test
    path('send-test-email/', views.send_test_email, name="test_mail")
]