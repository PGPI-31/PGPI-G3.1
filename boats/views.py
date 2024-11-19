from django.shortcuts import get_object_or_404, render, redirect
from .models import BoatInstance, BoatModel
from .forms import BoatInstanceForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

def listar_modelos(request):
    modelos = BoatModel.objects.all()
    return render(request, 'listar_modelos.html', {'modelos': modelos})

def listar_productos(request):
    productos = BoatInstance.objects.all()
    return render(request, 'listar_instancias.html', {'productos': productos})


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

def mostrar_modelo(request, model_id):
    boat_model = get_object_or_404(BoatModel, id=model_id)
    boat_instances = boat_model.instances.all()
    context = {
        'boat_model': boat_model,
        'boat_instances': boat_instances,
    }
    return render(request, 'mostrar_modelo.html', context)
