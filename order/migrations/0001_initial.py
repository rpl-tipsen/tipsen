# Generated by Django 4.2.7 on 2023-12-02 04:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
        ('payment', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('userprofile', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_special_order', models.BooleanField(default=False)),
                ('timestamp', models.TimeField(auto_now_add=True)),
                ('status', models.CharField(max_length=20)),
                ('quantity', models.IntegerField()),
                ('description', models.TextField(max_length=150)),
                ('ongkir', models.IntegerField(default=0)),
                ('other_fee', models.IntegerField(default=0)),
                ('subtotal', models.BigIntegerField()),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='userprofile.address')),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('payment', models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, to='payment.payment')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='products.product')),
            ],
        ),
    ]