# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('add/<int:boat_id>/', views.add_to_cart, name='adicion_cesta'),
    path('add_catalogue/<int:model_id>/', views.add_to_cart_catalogue, name='adicion_cesta_catalogo'),
    path('add_quantity/<str:group_key>/', views.add_quantity, name='add_quantity'),
    path('subtract_quantity/<str:group_key>/', views.subtract_quantity, name='subtract_quantity'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('', views.view_cart, name='mostrar_cesta'),

]
