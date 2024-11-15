# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.mostrar_productos, name='mostrar_productos'),
]