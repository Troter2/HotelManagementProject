

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Reception', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RestaurantReservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customers_names', models.CharField(max_length=100)),
                ('customer_contact', models.CharField(max_length=100)),
                ('number_guests', models.IntegerField(default=0)),
                ('date_reservation', models.DateField()),
                ('room_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Reception.room')),
            ],
        ),
    ]
