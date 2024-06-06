import uuid

from django.db import models
from django.db.models.functions import datetime

from Reception.models import Room, RoomReservation, CustomUser


# Create your models here.


class Order(models.Model):
    date = models.DateField(default=datetime.datetime.now)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    identifier = models.CharField(max_length=5, default='0000A', editable=True)
    is_paid = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.identifier = self.generate_identifier()
        super().save(*args, **kwargs)

    def generate_identifier(self):
        last_order = Order.objects.all().order_by('id').last()
        if last_order:
            last_identifier = last_order.identifier
            last_number = int(last_identifier[:4])
            last_letter = last_identifier[4]
            new_number = (last_number + 1) % 10000
            new_letter = last_letter
            if new_number == 0:
                new_letter = chr((ord(last_letter) + 1 - 65) % 26 + 65)
            new_identifier = f'{new_number:04d}{new_letter}'
        else:
            new_identifier = '0000A'
        return new_identifier


class Item(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    active = models.BooleanField(default=True)
    img = models.ImageField(upload_to='item_photo/')


class ItemAmount(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    amount = models.IntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE)


class RestaurantReservation(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    client_name = models.CharField(max_length=100)
    room_reservation = models.ForeignKey(RoomReservation, on_delete=models.CASCADE, blank=True, null=True)
    entrance_hours = models.TimeField()
    date_entrance = models.DateField()
    costumers_number = models.IntegerField(default=0)
    validated = models.BooleanField(default=False)
    order_num = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
