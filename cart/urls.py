# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('cesta/', views.CartInstanceForm, name='crear_cesta'),
    path('cesta/', views.CartInstanceForm, name='add_item'),

]