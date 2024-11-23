from django import forms
from .models import BoatInstance, BoatType, BoatModel, Port


class BoatInstanceForm(forms.ModelForm):

    class Meta:
        model = BoatInstance
        fields = ['model', 'name', 'port', 'available']
        labels = {
            'model': 'Modelo',
            'name': 'Nombre',
            'port': 'Puerto',
            'available': 'Disponible',
            'price_per_day': 'Precio por día',
        }


class BoatTypeForm(forms.ModelForm):
    
    class Meta:
        model = BoatType
        fields = ['name', 'description']
        labels = {
            'bnane': 'Nombre',
            'description': 'Descripción'
        }



class BoatModelForm(forms.ModelForm):
    
    class Meta:
        model = BoatModel
        fields = ['boat_type', 'name', 'capacity', 'brand', 'image', 'price_per_day']
        labels = {
            'boat_type': 'Tipo de embarcación',
            'name': 'Nombre',
            'capacity': 'Capacidad',
            'brand': 'Marca',
            'image': 'Imagen',
        }


class PortForm(forms.ModelForm):
    
    class Meta:
        model = Port
        fields = ['name', 'address']
        labels = {
            'name': 'Nombre',
            'address': 'Dirección',
        }
