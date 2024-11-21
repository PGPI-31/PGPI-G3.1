from django import forms
from .models import BoatInstance, BoatType, BoatModel, Port


class BoatInstanceForm(forms.ModelForm):

    class Meta:
        model = BoatInstance
        fields = ['model', 'name', 'port', 'available', 'price_per_day']
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


class BoatModelForm(forms.ModelForm):
    
    class Meta:
        model = BoatModel
        fields = ['boat_type', 'name', 'capacity', 'brand', 'image']


class PortForm(forms.ModelForm):
    
    class Meta:
        model = Port
        fields = ['name', 'address']
