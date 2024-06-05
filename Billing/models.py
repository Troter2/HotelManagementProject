from django.db import models
from Reception.models import RoomReservation


# Create your models here.

class Billing(models.Model):
    total_amount = models.IntegerField()
    date = models.DateField()
    room_information = models.ForeignKey(RoomReservation, on_delete=models.CASCADE)


class Coupon(models.Model):
    discount_code = models.IntegerField(max_length=20)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    active = models.BooleanField(default=True)


class Promotion(models.Model):
    image = models.ImageField(upload_to='media/promotion/')
    title = models.CharField(max_length=100)
    description = models.TextField()
    discount_code = models.ForeignKey(Coupon, on_delete=models.CASCADE)
