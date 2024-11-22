# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('add/<int:boat_id>/', views.add_to_cart, name='adicion_cesta'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('', views.view_cart, name='mostrar_cesta'),

]
