from django.db import models


# Create your models here.
class RoomReservation(models.Model):
    reservation_number = models.CharField(max_length=100)
    DNI = models.CharField(max_length=10, unique=True)
    guests_name = models.CharField(max_length=100)
    guests_surname = models.CharField(max_length=100)
    guests_email = models.EmailField()
    guests_phone = models.CharField(max_length=100)
    guest_checkin = models.DateField()
    guest_checkout = models.DateField()
    guests_number = models.IntegerField()
    # room_type = lo de creus
    price = models.DecimalField(max_digits=10, decimal_places=2)
