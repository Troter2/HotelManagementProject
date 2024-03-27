from django.db import models
from Reception.models import RoomReservation


# Create your models here.

class Billing(models.Model):
    total_amount = models.IntegerField()
    date = models.DateField()
    room_information = models.ForeignKey(RoomReservation, on_delete=models.CASCADE)
