# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('add_to_cart/<int:boat_id>/', views.add_to_cart, name='adicion_cesta'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('cesta/', views.view_cart, name='mostrar_cesta'),

]
