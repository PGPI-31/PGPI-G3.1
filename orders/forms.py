from django import forms

from orders.models import Pago

class ClientDataForm(forms.Form):
    name = forms.CharField(label='Nombre', max_length=30, required=True)
    surname = forms.CharField(label='Apellido', max_length=30, required=True)
    telephone = forms.CharField(label='Teléfono', max_length=15, required=True)
    email = forms.EmailField(label='Correo electrónico', required=True)
    address = forms.CharField(label='Dirección', max_length=255, required=True)
    dni = forms.CharField(label='DNI', max_length=10, required=True)
    birthdate = forms.DateField(label='Fecha de nacimiento', widget=forms.DateInput(attrs={'type': 'date'}), required=True)

class PaymentMethodForm(forms.Form):
    method = forms.ChoiceField(
        choices=Pago.PAYMENT_METHOD_CHOICES,
        label="Método de Pago",
        widget=forms.Select
    )