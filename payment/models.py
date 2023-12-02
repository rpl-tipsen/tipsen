from django.db import models
from django.core.validators import RegexValidator


class Payment(models.Model):
    payment_reference_number = models.CharField(max_length=69)
    timestamp = models.TimeField(auto_now_add=True)
    jumlah = models.BigIntegerField()

    bank_validator = RegexValidator(
        regex=r"BCA|Mandiri|BNI", message="TipSen hanya menggunakan Bank BCA, Mandiri dan BNI"
    )

    image_validator = RegexValidator(
        regex=r"https:\/\/[a-zA-Z0-9.-]+\.supabase\.co\/[^\/]+\/[^\/]+\.(png|jpeg|jpg)",
        message="image can only be from",
    )

    image_link = models.CharField(validators=[image_validator])

    bank = models.CharField(validators=[bank_validator])
