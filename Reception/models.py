from django.db import models


class RoomType(models.Model):
    name = models.CharField(max_length=255)
    capacity = models.IntegerField()
    photo = models.ImageField(upload_to='room_photos/')
    description = models.TextField()


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
    guests_number = models.IntegerField(default=0)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)




class Room(models.Model):
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, null=True)
    room_number = models.CharField(max_length=50)
    is_clean = models.BooleanField(default=True)

