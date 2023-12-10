# Generated by Django 4.2.7 on 2023-12-10 13:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('userprofile', '0002_address_is_active'),
        ('payment', '0003_alter_payment_bank'),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/')),
            ],
        ),
        migrations.CreateModel(
            name='OrderStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('is_special_request', models.BooleanField(default=False)),
                ('timestamp', models.TimeField(auto_now_add=True)),
                ('quantity', models.IntegerField()),
                ('description', models.TextField(max_length=150)),
                ('ongkir', models.IntegerField(default=0)),
                ('other_fee', models.IntegerField(default=0)),
                ('subtotal', models.BigIntegerField()),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='userprofile.address')),
                ('payment', models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, to='payment.payment')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='products.product')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='order.orderstatus')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
