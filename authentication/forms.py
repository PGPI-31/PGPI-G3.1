from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.contrib.auth.forms import AuthenticationForm

class UserRegisterForm(UserCreationForm):
    birthdate = forms.DateField(label="Birthdate (format: YYYY-MM-DD)", widget=forms.DateInput(format='%Y-%m-%d'))
    class Meta:
        model = User
        fields = ['username', 'email', 'telephone', 'address', 'dni', 'birthdate', 'password1', 'password2']

class UserLoginForm(AuthenticationForm):
    pass