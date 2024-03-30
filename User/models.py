from django.db import models

from Reception.models import RoomReservation


# Create your models here.


class Shift(models.Model):
    user = models.CharField(max_length=16)
    password = models.CharField(max_length=50)
    shift = models.DateTimeField()


class Customer(models.Model):
    name = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    DNI = models.CharField(max_length=9)
    reservation = models.ForeignKey(RoomReservation, on_delete=models.CASCADE)

