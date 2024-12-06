from django.shortcuts import get_object_or_404, render, redirect
from .models import BoatInstance, BoatModel, BoatType, Port
from .forms import BoatInstanceForm, BoatTypeForm, BoatModelForm, PortForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.db.models import Count, Q, Case, When, IntegerField, Prefetch, F
from orders.models import OrderBoat
from datetime import datetime
from collections import defaultdict


def ver_catalogo(request):
    title = request.GET.get('title')  # Nombre del barco
    boat_type = request.GET.get('boat_type')  # ID del tipo de barco
    port = request.GET.get('port')  # ID del puerto
    modelos = BoatModel.objects.all()
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    boats = BoatInstance.objects.all()
    unavailable_boats = set() 
    # Filtrar por título si se proporciona
    if title:
        modelos = modelos.filter(name__icontains=title)

    # Filtrar por tipo de barco si se proporciona
    if boat_type:
        modelos = modelos.filter(boat_type_id=boat_type, instances__available=True).distinct()

    # Filtrar por puerto si se proporciona
    if port and port is not None and port != '':
        modelos = modelos.filter(instances__port_id=port, instances__available=True).distinct()

    if start_date and end_date:
        start = datetime.strptime(start_date, "%Y-%m-%d").date()
        end = datetime.strptime(end_date, "%Y-%m-%d").date()
        for modelo in modelos:
            # Retrieve all instances for the current model and port (if provided)
            instances = modelo.instances.filter(available=True)
            if port:
                instances = instances.filter(port_id=port)

            # Initialize the count of available instances
            available_count = 0

            for instance in instances:
                # Get all orders for this instance
                orders = instance.order_boats.all()

                # Check if the instance is free within the date range
                if not any(order.start_date < end and order.end_date > start for order in orders):
                    available_count += 1

            # Annotate the model with the calculated count
            modelo.available_within_dates = available_count
    else:
        # Default: All models considered available within date range
        modelos = modelos.annotate(
            available_within_dates=Case(
                When(pk__isnull=False, then=1),  # All models available if no date selected
                default=0,
                output_field=IntegerField()
            )
        )
    
    boat_types = BoatType.objects.all()
    ports = Port.objects.all()

    instance_counts = defaultdict(int)
    for modelo in modelos:
        for instance in modelo.instances.all():
            if instance.available:
                key = f"{modelo.id}_{instance.port_id}"  # Create a unique string key
                instance_counts[key] += 1
    
    context = {
        'modelos': modelos,
        'ports': ports,
        'boat_types': boat_types,
        'unavailable_boats': unavailable_boats,
        'instance_counts': dict(instance_counts)
    }
    return render(request, 'catalogo.html', context)


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


@login_required
def modify_port(request, port_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden("No tienes permiso para modificar puertos.")
    
    port = get_object_or_404(Port, id=port_id)

    if request.method == 'POST':
        form = PortForm(request.POST, instance=port)
        if form.is_valid():
            form.save()
            return redirect('listar_puertos')  
    else:
        form = PortForm(instance=port)
        
    return render(request, 'admin/modify_port.html', {'form': form})

@login_required
def modify_boat_type(request, type_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden("No tienes permiso para modificar el tipo de barco.")
    
    boat_type = get_object_or_404(BoatType, id=type_id)

    if request.method == 'POST':
        form = BoatTypeForm(request.POST, instance=boat_type)
        if form.is_valid():
            form.save()
            return redirect('listar_tipos')  
    else:
        form = BoatTypeForm(instance=boat_type)        
    return render(request, 'admin/modify_boat_type.html', {'form': form})


@login_required
def modify_boat_model(request, model_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden("No tienes permiso para modificar modelos de barcos.")
    
    boat_model = get_object_or_404(BoatModel, id=model_id)

    if request.method == 'POST':
        form = BoatModelForm(request.POST, request.FILES,instance=boat_model)
        if form.is_valid():
            form.save()
            return redirect('listar_modelos')
    else:
        form = BoatModelForm(instance=boat_model)

    return render(request, 'admin/modify_boat_model.html', {'form': form})

@login_required
def modify_boat_instance(request,boat_instance_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden("No tienes permiso para modificar una instancia de barco.")
    boat_instance = get_object_or_404(BoatInstance, id=boat_instance_id)

    if request.method == 'POST':
        form = BoatInstanceForm(request.POST,instance=boat_instance)
        if form.is_valid():
            form.save()
            return redirect('listar_productos')
    else:
        form = BoatInstanceForm(instance=boat_instance)

    return render(request, 'admin/modify_boat_instance.html', {'form': form})


def mostrar_modelo(request, model_id):
    boat_model = get_object_or_404(BoatModel, id=model_id)
    boat_instances = boat_model.instances.all()
    context = {
        'boat_model': boat_model,
        'boat_instances': boat_instances,
    }
    return render(request, 'mostrar_modelo.html', context)