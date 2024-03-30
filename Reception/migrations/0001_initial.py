# Generated by Django 5.0.3 on 2024-03-30 14:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_number', models.CharField(max_length=50)),
                ('is_clean', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='RoomType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('capacity', models.IntegerField()),
                ('photo', models.ImageField(upload_to='room_photos/')),
                ('description', models.TextField()),
                ('square_meter', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='RoomReservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reservation_number', models.CharField(max_length=100)),
                ('DNI', models.CharField(max_length=10, unique=True)),
                ('guests_name', models.CharField(max_length=100)),
                ('guests_surname', models.CharField(max_length=100)),
                ('guests_email', models.EmailField(max_length=254)),
                ('guests_phone', models.CharField(max_length=100)),
                ('guest_checkin', models.DateField(blank=True, null=True)),
                ('guest_checkout', models.DateField(blank=True, null=True)),
                ('guest_is_here', models.BooleanField(default=False)),
                ('guests_number', models.IntegerField(default=0)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('room_is_payed', models.BooleanField(default=False)),
                ('room_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Reception.room')),
            ],
        ),
        migrations.AddField(
            model_name='room',
            name='room_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Reception.roomtype'),
        ),
    ]
