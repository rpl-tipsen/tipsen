# Generated by Django 4.2.7 on 2023-11-30 08:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_userprofile'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
