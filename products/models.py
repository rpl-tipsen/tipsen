from django.db import models
from django.core.validators import RegexValidator
# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    description = models.TextField()

    image_link_validator = RegexValidator(
        regex=r'^https?://.*\.(jpeg|jpg|png)$',
        message='Image must be from http or https with jpg, jpeg or png extension',
        code='invalid_image_link'
    )

    image_link = models.CharField(
        validators=[image_link_validator]
    )
