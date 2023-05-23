from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('user/',views.user, name='user'),
    path('profile_settings', views.account_settings, name = 'account_settings'),
    path('', views.dashboard, name='dashboard'),
    path('products/', views.products, name="products"), 
    path('customers/', views.customers, name="customers"),
    path('customers/<str:pk>', views.customers_unique, name="customers_unique"),
    path('create_order/',views.createOrder, name="create_order"),
    path('create_customer/',views.createCustomer, name="create_customer"),
    path('update_customer/<str:pk>', views.updateCustomer, name ="update_customer"),
    path('delete_customer/<str:pk>', views.deleteCustomer, name ="delete_customer"),
    path('customer_order/<str:pk>', views.customerOrder, name="customer_order")
]