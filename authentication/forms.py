from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

class UserRegisterForm(UserCreationForm):
    birthdate = forms.DateField(label="Fecha de nacimiento (YYYY-MM-DD)", widget=forms.DateInput(format='%Y-%m-%d'))
    username = forms.CharField(label="Nombre", max_length=100)
    email = forms.CharField(label="Email", max_length=100)
    telephone = forms.CharField(label="Número de teléfono", max_length=9)
    address = forms.CharField(label="Dirección", max_length=500)
    dni = forms.CharField(label="DNI", max_length=9)
    password1 = forms.CharField(label="Contraseña", max_length=20, widget=forms.PasswordInput(attrs={'placeholder': ''}))
    password2 = forms.CharField(label="Repite la contraseña", max_length=20, widget=forms.PasswordInput(attrs={'placeholder': ''}))

    class Meta:
        model = User
        fields = ['username', 'email', 'telephone', 'address', 'dni', 'birthdate', 'password1', 'password2']
    
class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label = "Nombre", max_length=100)
    password = forms.CharField(label = "Contraseña", max_length=20, widget=forms.PasswordInput(attrs={'placeholder': ''}))
