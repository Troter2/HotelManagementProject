from django.db import models
from Reception.models import Room, RoomReservation


# Create your models here.
class RestaurantReservation(models.Model):
    customers_names = models.CharField(max_length=100)
    room_number = models.ForeignKey(Room, on_delete=models.CASCADE)
    customer_contact = models.CharField(max_length=100)
    number_guests = models.IntegerField(default=0)
    date_reservation = models.DateField()
class RestaurantReservation_v2(models.Model):
    client_name = models.CharField(max_length=100)
    room_reservation = models.ForeignKey(RoomReservation, on_delete=models.CASCADE)
    entrance_hours = models.TimeField()
    date_entrance = models.DateField()
    costumers_number = models.IntegerField(default=0)