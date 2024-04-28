import uuid

from django.db import models
from django.db.models.functions import datetime

from Reception.models import Room, RoomReservation


# Create your models here.

class Dish(models.Model):
    PRIMER_PLATO_CHOICES = [
        ('gazpacho', 'Gazpacho las palmeras'),
        ('ensalada', 'Ensalada mediterránea'),
        ('huevos', 'Huevos a la flamenca'),
        ('canelones', 'Canelones de foie'),
        ('arroz_negro', 'Arroz negro'),
    ]

    SEGUNDO_PLATO_CHOICES = [
        ('pollo', 'Pollo asado con champiñones'),
        ('merluza', 'Merluza en salsa rusa'),
        ('tortilla', 'Tortilla de espinacas con zanahorias'),
        ('albondigas', 'Albóndigas a la jardinera con verduritas'),
        ('tortilla_patata', 'Tortilla de patata con champiñones'),
    ]

    POSTRE_CHOICES = [
        ('helado', 'Helado'),
        ('tarta_queso', 'Tarta de queso'),
        ('music', 'Music'),
        ('crema_catalana', 'Crema catalana'),
        ('flam', 'Flam de huevo'),
    ]

    REFRESCO_CHOICES = [
        ('fanta_limon', 'Fanta limón'),
        ('fanta_naranja', 'Fanta naranja'),
        ('coca_cola_zero', 'Coca-Cola Zero'),
        ('coca_cola', 'Coca-Cola'),
        ('aquarius_limon', 'Aquarius de limón'),
        ('cerveza', 'Cerveza'),
        ('vino_gaseosa', 'Vino-gaseosa'),
    ]

    TIPO_CHOICES = [
        ('primer_plat', 'Primer Plato'),
        ('segon_plat', 'Segundo Plato'),
        ('postre', 'Postre'),
        ('refresc', 'Refresco'),
    ]

    tipus = models.CharField(max_length=20, choices=TIPO_CHOICES)
    nom = models.CharField(max_length=100,
                           choices=PRIMER_PLATO_CHOICES + SEGUNDO_PLATO_CHOICES + POSTRE_CHOICES + REFRESCO_CHOICES)
    descripcio = models.TextField()
    preu = models.DecimalField(max_digits=10, decimal_places=2)


class Order(models.Model):
    date = models.DateField(default=datetime.datetime.now)
    total = models.DecimalField(max_digits=10, decimal_places=2)


class Item(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    active = models.BooleanField(default=True)
    img = models.ImageField(upload_to='room_photos/')


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
