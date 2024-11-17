from django import forms
from .models import BoatInstance


class BoatInstanceForm(forms.ModelForm):

    class Meta:
        model = BoatInstance
        fields = ['model', 'name', 'port', 'available', 'price_per_day']

