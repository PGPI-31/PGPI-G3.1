# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('create-order/', views.create_order, name='create_order'),
    path('client-data/', views.collect_client_data, name='collect_client_data'),
    path('payment-method/', views.select_paymnet_method, name='select_payment_method'),
    path('online-payment/', views.online_payment, name='online_payment'),
    path('order-complete/', views.order_complete, name='order_complete'),
]