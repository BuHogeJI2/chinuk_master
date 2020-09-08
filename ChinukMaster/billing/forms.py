from django import forms
from .models import *

class ClientForm(forms.ModelForm):
    
    class Meta:
        model = Client
        fields = '__all__'

class PaymentForm(forms.ModelForm):

    class Meta:
        model = Payment
        fields = '__all__'

class TrenerForm(forms.ModelForm):

    class Meta:
        model = Trener
        fields = '__all__'

class GroupForm(forms.ModelForm):

    class Meta:
        model = Group
        fields = '__all__'

class AddressForm(forms.ModelForm):

    class Meta:
        model = Address
        fields = '__all__'
