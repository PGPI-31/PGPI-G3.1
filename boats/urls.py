# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('modelos/', views.listar_modelos, name='listar_modelos'),
    path('catalogo/', views.ver_catalogo, name='ver_catalogo'),
    path('modelos/create/', views.create_boat_model, name='crear_modelo'),
    path('modelos/modify/<int:model_id>', views.modify_boat_model, name='modificar_modelo'),
    path('tipos/', views.listar_tipos, name='listar_tipos'),
    path('tipos/create', views.create_boat_type, name='crear_tipo'),
    path('tipos/modify/<int:type_id>', views.modify_boat_type, name='modificar_tipo'),
    path('puertos/', views.listar_puertos, name='listar_puertos'),
    path('puertos/create/', views.create_port, name='crear_puerto'),
    path('puertos/modify/<int:port_id>', views.modify_port, name='modificar_puerto'),
    path('', views.listar_productos, name='listar_productos'),
    path('create/', views.create_boat_instance, name='crear_productos'),
    path('modify/<int:boat_instance_id>', views.modify_boat_instance, name='modificar_productos'),
    path('modelos/<int:model_id>/', views.mostrar_modelo, name='mostrar_modelo'),
]
