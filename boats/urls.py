# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('productos/', views.mostrar_productos, name='mostrar_productos'),
]