from django import forms
from .models import Cart, CartItem


class CartInstanceForm(forms.ModelForm):

    class Meta:
        model = Cart
        fields = ['created_at', 'updated_at', 'start_date', 'end_date', 'user_id']
        labels = {
            'created_at': 'Creación',
            'updated_at': 'Actualización',
            'start_date': 'Comienzo',
            'end_date': 'Finalización',
            'user_id': 'Cliente',
        }

class CartItemInstanceForm(forms.ModelForm):

    class Meta:
        model = CartItem
        fields = ['number_of_days', 'price_per_day', 'total_price', 'boat_instance_id', 'cart_id']
        labels = {
            'number_of_days': 'Días de duración',
            'price_per_day': 'Precio diario',
            'total_price': 'Precio total',
            'boat_instance_id': 'Barco',
            'cart_id': 'Cesta',
        }