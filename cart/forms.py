from django import forms
from .models import Cart, CartItem


class CartInstanceForm(forms.ModelForm):

    class Meta:
        model = Cart
        fields = ['model', 'name', 'port', 'available', 'price_per_day']
        labels = {
            'model': 'Modelo',
            'name': 'Nombre',
            'port': 'Puerto',
            'available': 'Disponible',
            'price_per_day': 'Precio por día',
        }

class CartItemInstanceForm(forms.ModelForm):

    class Meta:
        model = CartItem
        fields = ['model', 'name', 'port', 'available', 'price_per_day']
        labels = {
            'model': 'Modelo',
            'name': 'Nombre',
            'port': 'Puerto',
            'available': 'Disponible',
            'price_per_day': 'Precio por día',
        }