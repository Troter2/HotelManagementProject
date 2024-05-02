from django.db import models
from Reception.models import Room


# Create your models here.
class RestaurantReservation(models.Model):
    customers_names = models.CharField(max_length=100)
    room_number = models.ForeignKey(Room, on_delete=models.CASCADE)
    customer_contact = models.CharField(max_length=100)
    number_guests = models.IntegerField(default=0)
    date_reservation = models.DateField()
