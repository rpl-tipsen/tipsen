from django.db import models
from django.core.validators import RegexValidator
from authentication.models import AuthUser


class UserProfile(models.Model):
    user = models.OneToOneField(AuthUser, on_delete=models.RESTRICT)
    fullname = models.CharField(max_length=69)
    birthdate = models.DateField(default="1970-01-01")


class Address(models.Model):
    user = models.ForeignKey(to=AuthUser, on_delete=models.CASCADE)
    receiver_name = models.CharField(blank=False, max_length=50)
    address = models.TextField(max_length=100)
    city = models.CharField(blank=False)
    is_active = models.BooleanField(default=True)

    phone_number_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",  # Customize the regex based on your requirements
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
    )

    postal_code_validator = RegexValidator(
        regex=r"^\d{5}$", message="Postal Code must be numerical strings consisting of 5 numbers"
    )

    postal_code = models.CharField(max_length=5, validators=[postal_code_validator])
    phone_number = models.CharField(
        validators=[phone_number_regex],
        max_length=15,
    )
