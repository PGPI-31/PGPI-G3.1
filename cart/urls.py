# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('add_to_cart/<int:boat_id>/', views.add_to_cart, name='adjuntar_cesta'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='eliminar_cesta'),
    path('checkout/', views.checkout, name='adquirir'),
]
