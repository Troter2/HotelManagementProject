import datetime

from django.db import models
from django.utils import timezone


class RoomType(models.Model):
    name = models.CharField(max_length=255)
    capacity = models.IntegerField()
    photo = models.ImageField(upload_to='room_photos/')
    description = models.TextField()
    square_meter = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Room(models.Model):
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, null=True)
    room_number = models.CharField(max_length=50)
    is_clean = models.BooleanField(default=False)

    def __str__(self):
        return self.room_number


# Create your models here.
class RoomReservation(models.Model):
    reservation_number = models.CharField(max_length=100)
    DNI = models.CharField(max_length=9)
    guests_name = models.CharField(max_length=100)
    guests_surname = models.CharField(max_length=100)
    guests_email = models.EmailField()
    guests_phone = models.CharField(max_length=100)
    guest_checkin = models.DateField(null=True, blank=True)
    guest_checkout = models.DateField(null=True, blank=True)
    guest_checkin_hour = models.TimeField(null=False, default=datetime.time(13, 0, 0))
    guest_checkout_hour = models.TimeField(null=False, default=datetime.time(10, 0, 0))
    guest_is_here = models.BooleanField(default=False)
    guests_number = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    room_number = models.ForeignKey(Room, on_delete=models.CASCADE)
    room_is_payed = models.BooleanField(default=False)

def get_current_date():
    return timezone.now().date()
def get_current_hour():
    return timezone.now

class LostItem(models.Model):
    item_name = models.CharField(max_length=100)
    encounter_hour = models.TimeField(default=get_current_date)
    encounter_date = models.DateField(default=get_current_date)
    in_possesion = models.BooleanField(default=True)
