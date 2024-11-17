from django.shortcuts import render, redirect
from .models import BoatInstance
from .forms import BoatInstanceForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden


# Create your views here.
def mostrar_productos(request):
    productos = BoatInstance.objects.all()
    return render(request, 'listar_todo.html', {'productos': productos})


@login_required
def create_boat_instance(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You do not have permission to create a boat instance.")
    if request.method == 'POST':
        form = BoatInstanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mostrar_productos')
    else:
        form = BoatInstanceForm()

    return render(request, 'create_boat_instance.html', {'form': form})
