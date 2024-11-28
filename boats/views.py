from django.shortcuts import get_object_or_404, render, redirect
from .models import BoatInstance, BoatModel, BoatType, Port
from .forms import BoatInstanceForm, BoatTypeForm, BoatModelForm, PortForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.db.models import Q
from orders.models import OrderBoat
from datetime import datetime


def ver_catalogo(request):
    modelos = BoatModel.objects.all()
    ports = Port.objects.all()
    return render(request, 'catalogo.html', {'modelos': modelos, 'ports': ports})


def listar_modelos(request):
    modelos = BoatModel.objects.all()
    return render(request, 'listar_modelos.html', {'modelos': modelos})


def listar_productos(request):
    productos = BoatInstance.objects.all()
    return render(request, 'listar_instancias.html', {'productos': productos})


def listar_tipos(request):
    tipos = BoatType.objects.all()
    return render(request, 'admin/listar_tipos.html', {'tipos':tipos})


def listar_puertos(request):
    puertos = Port.objects.all()
    return render(request, 'admin/listar_puertos.html', {'puertos': puertos})


@login_required
def create_boat_instance(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("No tienes permiso para crear una instancia de barco.")
    if request.method == 'POST':
        form = BoatInstanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_productos')
    else:
        form = BoatInstanceForm()

    return render(request, 'admin/create_boat_instance.html', {'form': form})


@login_required
def create_boat_type(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("No tienes permiso para crear tipos de barcos.")
    if request.method == 'POST':
        form = BoatTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_tipos')
    else:
        form = BoatTypeForm()

    return render(request, 'admin/create_boat_type.html', {'form': form})


@login_required
def create_boat_model(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("No tienes permiso para crear modelos de barcos.")
    if request.method == 'POST':
        form = BoatModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('listar_modelos')
    else:
        form = BoatModelForm()

    return render(request, 'admin/create_boat_model.html', {'form': form})


@login_required
def create_port(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("No tienes permiso para crear puertos.")
    if request.method == 'POST':
        form = PortForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_puertos')
    else:
        form = PortForm()

    return render(request, 'admin/create_port.html', {'form': form})


def mostrar_modelo(request, model_id):
    boat_model = get_object_or_404(BoatModel, id=model_id)
    boat_instances = boat_model.instances.all()
    context = {
        'boat_model': boat_model,
        'boat_instances': boat_instances,
    }
    return render(request, 'mostrar_modelo.html', context)


def filter_boats(request):
    """
    Filtra las instancias de barcos según los criterios especificados.
    """
    title = request.GET.get('title')  # Nombre del barco
    boat_type = request.GET.get('boat_type')  # ID del tipo de barco
    port = request.GET.get('port')  # ID del puerto
    date = request.GET.get('date')  # Fecha de disponibilidad

    # Base query: todos los barcos
    boats = BoatInstance.objects.all()

    # Filtrar por título si se proporciona
    if title:
        boats = boats.filter(name__icontains=title)

    # Filtrar por tipo de barco si se proporciona
    if boat_type:
        boats = boats.filter(model__boat_type_id=boat_type)

    # Filtrar por puerto si se proporciona
    if port:
        boats = boats.filter(port_id=port)

    # Filtrar por disponibilidad en una fecha específica
    unavailable_boats = set()  # Usamos un conjunto para almacenar los barcos no disponibles
    if date:
        try:
            date = datetime.strptime(date, '%Y-%m-%d').date()  # Convertir fecha a objeto
            reserved_boats = OrderBoat.objects.filter(
                Q(start_date__lte=date) & Q(end_date__gte=date)
            ).values_list('boat_id', flat=True)
            # Los barcos reservados se marcan como no disponibles
            unavailable_boats.update(reserved_boats)
        except ValueError:
            # Si la fecha no tiene formato válido, no filtrar por fecha
            pass

    # Obtener todos los tipos de barcos y puertos para los filtros
    boat_types = BoatType.objects.all()
    ports = Port.objects.all()

    # Renderizar el catálogo con filtros y resultados
    return render(request, 'catalogo.html', {
        'modelos': boats,
        'boat_types': boat_types,
        'ports': ports,
        'unavailable_boats': unavailable_boats,
    })
