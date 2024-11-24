# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('create-order/', views.create_order, name='create_order'),
    path('client-data/', views.collect_client_data, name='collect_client_data'),
    path('payment-method/', views.select_paymnet_method, name='select_payment_method'),
    path('order-complete/', views.order_complete, name='order_complete'),

    # Stripe
    path('stripe-payment/', views.stripe_payment, name='stripe_payment'),
    path("payment/success/", views.payment_success, name="payment_success"),
    path("payment/cancel/", views.payment_cancel, name="payment_cancel"),
    path("webhook", views.stripe_webhook, name="stripe_webhook"),
]