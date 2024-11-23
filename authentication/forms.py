from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.contrib.auth.forms import AuthenticationForm

class UserRegisterForm(UserCreationForm):
    birthdate = forms.DateField(
        label="Fecha de nacimiento (formato: AAAA-MM-DD)",
        widget=forms.DateInput(format='%Y-%m-%d')
    )

    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput,
        help_text="La contraseña debe tener al menos 8 caracteres y no puede ser totalmente numérica."
    )
    password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput,
        help_text="Ingrese la misma contraseña que arriba para verificarla."
    )
    
    class Meta:
        model = User
        fields = ['email', 'telephone', 'address', 'dni', 'birthdate', 'password1', 'password2']
        labels = {
            'email': 'Correo electrónico',
            'telephone': 'Teléfono',
            'address': 'Dirección',
            'dni': 'DNI',
            'birthdate': 'Fecha de nacimiento'
        }

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Correo electrónico"
        self.fields['password'].label = "Contraseña"