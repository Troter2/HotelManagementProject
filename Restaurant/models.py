from django.db import models


# Create your models here.
class RestaurantReservation(models.Model):
    customers_names = models.CharField(max_length=100)
    # Room reservation room_number = models.CharField(max_length=100)
    customer_contact = models.CharField(max_length=100)
    number_guests = models.IntegerField(default=0)
    date_reservation = models.DateField()
