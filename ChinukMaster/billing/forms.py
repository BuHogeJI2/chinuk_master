from django import forms
from .models import *

class ClientForm(forms.ModelForm):
    
    class Meta:
        model = Client
        fields = ('member_card', 'name', 'tel_number', 'info', 'cl_type', 'treners', 'groups')