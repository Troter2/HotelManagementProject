import uuid

from django.db import models
from django.db.models.functions import datetime

from Reception.models import Room, RoomReservation


# Create your models here.


class Order(models.Model):
    date = models.DateField(default=datetime.datetime.now)
    total = models.DecimalField(max_digits=10, decimal_places=2)


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
    client_name = models.CharField(max_length=100)
    room_reservation = models.ForeignKey(RoomReservation, on_delete=models.CASCADE, blank=True, null=True)
    entrance_hours = models.TimeField()
    date_entrance = models.DateField()
    costumers_number = models.IntegerField(default=0)
    validated = models.BooleanField(default=False)
    order_num = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
