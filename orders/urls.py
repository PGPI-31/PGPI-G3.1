# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('create-order/', views.create_order, name='create_order'),
    path('client-data/', views.collect_client_data, name='collect_client_data'),
    path('payment-method/', views.select_payment_method, name='select_payment_method'),
    path('order-complete/', views.order_complete, name='order_complete'),
    path('ver/<int:order_id>/', views.view_order, name='show_order'),
    path('listar', views.list_orders, name='list_orders'),

    # Stripe
    path('stripe-payment/', views.stripe_payment, name='stripe_payment'),
    path("payment/success/", views.payment_success, name="payment_success"),
    path("payment/cancel/", views.payment_cancel, name="payment_cancel"),
    path("webhook", views.stripe_webhook, name="stripe_webhook"),
]