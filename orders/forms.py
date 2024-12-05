from django import forms

from orders.models import Pago
from orders.models import Cliente
from orders.models import Order
from orders.models import OrderBoat

class ClientDataForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['name', 'surname', 'telephone', 'email', 'address', 'dni']
        
        widgets = {
            'birthdate': forms.DateInput(attrs={'type': 'date'}),  # Esto asegura que se use un campo tipo date para fecha
        }

        labels = {
            'name': 'Nombre',
            'surname': 'Apellido',
            'telephone': 'Teléfono',
            'email': 'Correo electrónico',
            'address': 'Dirección',
            'dni': 'DNI',
        }

        help_texts = {
            'name': 'Ingresa tu primer nombre.',
            'surname': 'Ingresa tu apellido.',
            'telephone': 'Ingresa tu número de teléfono.',
            'email': 'Ingresa tu dirección de correo electrónico.',
            'address': 'Ingresa tu dirección de residencia.',
            'dni': 'Ingresa tu número de DNI.',
        }

        error_messages = {
            'name': {
                'required': 'El nombre es obligatorio.',
                'max_length': 'El nombre no puede tener más de 30 caracteres.'
            },
            'surname': {
                'required': 'El apellido es obligatorio.',
                'max_length': 'El apellido no puede tener más de 30 caracteres.'
            },
            'telephone': {
                'required': 'El teléfono es obligatorio.',
                'max_length': 'El teléfono no puede tener más de 15 caracteres.'
            },
            'email': {
                'required': 'El correo electrónico es obligatorio.',
            },
            'address': {
                'required': 'La dirección es obligatoria.',
                'max_length': 'La dirección no puede exceder los 255 caracteres.'
            },
            'dni': {
                'required': 'El DNI es obligatorio.',
                'max_length': 'El DNI no puede exceder los 10 caracteres.'
            },
            
        }
        
class PaymentMethodForm(forms.Form):
    method = forms.ChoiceField(
        choices=Pago.PAYMENT_METHOD_CHOICES,
        label="Método de Pago",
        widget=forms.Select
    )
    

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']

    status = forms.ChoiceField(
        label="Estado del Pedido",
        choices=Order.STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )
   

class OrderBoatForm(forms.ModelForm):
    class Meta:
        model = OrderBoat
        fields = ['start_date', 'end_date', 'days', 'price_per_day']

    start_date = forms.DateField(
        label="Fecha de Inicio",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=True
    )

    end_date = forms.DateField(
        label="Fecha de Fin",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=True
    )

    days = forms.IntegerField(
        label="Número de Días",
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        required=True
    )

    price_per_day = forms.DecimalField(
        label="Precio por Día (€)",
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        required=True
    )