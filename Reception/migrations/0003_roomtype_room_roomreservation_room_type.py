# Generated by Django 5.0.3 on 2024-03-28 14:02

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Reception', '0002_alter_roomreservation_guests_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='RoomType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('capacity', models.IntegerField()),
                ('photo', models.ImageField(upload_to='room_photos/')),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_number', models.CharField(max_length=50)),
                ('is_clean', models.BooleanField(default=True)),
                ('room_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Reception.roomtype')),
            ],
        ),
        migrations.AddField(
            model_name='roomreservation',
            name='room_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Reception.roomtype'),
            preserve_default=False,
        ),
    ]