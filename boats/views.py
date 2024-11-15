from django.shortcuts import render
from .models import BoatInstance

# Create your views here.
def mostrar_productos(request):
    productos = BoatInstance.objects.all()
    return render(request, 'listar_todo.html', {'productos': productos})