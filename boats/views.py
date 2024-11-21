from django.shortcuts import get_object_or_404, render, redirect
from .models import BoatInstance, BoatModel, BoatType, Port
from .forms import BoatInstanceForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden


def listar_modelos(request):
    modelos = BoatModel.objects.all()
    return render(request, 'listar_modelos.html', {'modelos': modelos})


def listar_productos(request):
    productos = BoatInstance.objects.all()
    return render(request, 'listar_instancias.html', {'productos': productos})


def listar_tipos(request):
    tipos = BoatType.objects.all()
    return render(request, 'listar_tipos.html', {'tipos':tipos})


def listar_puertos(request):
    puertos = Port.objects.all()
    return render(request, 'listar_puertos.html', {'puertos': puertos})


@login_required
def create_boat_instance(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You do not have permission to create a boat instance.")
    if request.method == 'POST':
        form = BoatInstanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_productos')
    else:
        form = BoatInstanceForm()

    return render(request, 'create_boat_instance.html', {'form': form})


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

    return render(request, 'create_boat_type.html', {'form': form})


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

    return render(request, 'create_boat_model.html', {'form': form})


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

    return render(request, 'create_port.html', {'form': form})


def mostrar_modelo(request, model_id):
    boat_model = get_object_or_404(BoatModel, id=model_id)
    boat_instances = boat_model.instances.all()
    context = {
        'boat_model': boat_model,
        'boat_instances': boat_instances,
    }
    return render(request, 'mostrar_modelo.html', context)
