# Generated by Django 5.0.2 on 2024-04-28 21:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Billing', '0001_initial'),
        ('Reception', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='billing',
            name='room_information',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Reception.roomreservation'),
        ),
    ]
