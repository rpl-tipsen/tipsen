from django import forms
from userprofile.models import Address


class OrderFirstForm(forms.Form):
    address = forms.ModelChoiceField(
        queryset=Address.objects.all(), label='Alamat')
    quantity = forms.IntegerField(label='Jumlah Pesanan', min_value=1)


class OrderSecondForm(forms.Form):
    payment_method = forms.CharField(label='Metode Pembayaran')
    payment_reference = forms.CharField(label='Nomor Referensi Pembayaran')
