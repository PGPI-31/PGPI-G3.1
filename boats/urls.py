# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('modelos/', views.listar_modelos, name='listar_modelos'),
    path('modelos/create/', views.create_boat_model, name='crear_modelo'),
    path('tipos/', views.listar_tipos, name='listar_tipos'),
    path('tipos/create', views.create_boat_type, name='crear_tipo'),
    path('puertos/', views.listar_puertos, name='listar_puertos'),
    path('puertos/create/', views.create_port, name='crear_puerto'),
    path('', views.listar_productos, name='listar_productos'),
    path('create/', views.create_boat_instance, name='crear_productos'),
    path('modelos/<int:model_id>/', views.mostrar_modelo, name='mostrar_modelo'),

]
