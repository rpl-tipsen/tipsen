from django import forms
from django.core.validators import RegexValidator


class OrderFirstForm(forms.Form):
    address_id = forms.IntegerField(label='Id Alamat')
    quantity = forms.IntegerField(label='Jumlah Pesanan', min_value=1)


class OrderSecondForm(forms.Form):
    bank_validator = RegexValidator(
        regex=r"BCA|Mandiri|BNI", message="TipSen hanya menggunakan Bank BCA, Mandiri dan BNI"
    )

    bank = forms.CharField(validators=[bank_validator])
    payment_reference_number = forms.CharField(
        label='Nomor Referensi Pembayaran')
