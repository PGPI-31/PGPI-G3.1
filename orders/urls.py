# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('create-order/', views.create_order, name='create_order'),
    path('client-data/', views.collect_client_data, name='collect_client_data'),
    path('delivery-data/', views.collect_delivery_data, name='collect_delivery_data'),
]