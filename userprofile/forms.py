# yourapp/forms.py
from django import forms
from .models import Address


class AddressForm(forms.ModelForm):

    class Meta:
        model = Address
        fields = ['receiver_name', 'phone_number', 'address', 'city', 'postal_code']

