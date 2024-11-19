# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('modelos/', views.listar_modelos, name='listar_modelos'),
    path('productos/', views.listar_productos, name='listar_productos'),
    path('create/', views.create_boat_instance, name='crear_productos'),
    path('modelos/<int:model_id>/', views.mostrar_modelo, name='mostrar_modelo'),
]
