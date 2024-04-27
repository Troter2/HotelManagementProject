
from django.db import models
from Reception.models import Room, RoomReservation


# Create your models here.
class RestaurantReservation(models.Model):
    customers_names = models.CharField(max_length=100)
    room_number = models.ForeignKey(Room, on_delete=models.CASCADE)
    customer_contact = models.CharField(max_length=100)
    number_guests = models.IntegerField(default=0)
    date_reservation = models.DateField()


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
    nom = models.CharField(max_length=100,choices=PRIMER_PLATO_CHOICES + SEGUNDO_PLATO_CHOICES + POSTRE_CHOICES + REFRESCO_CHOICES)
    descripcio = models.TextField()
    preu = models.DecimalField(max_digits=10, decimal_places=2)

class RestaurantReservation_v2(models.Model):
    client_name = models.CharField(max_length=100)
    room_reservation = models.ForeignKey(RoomReservation, on_delete=models.CASCADE)
    entrance_hours = models.TimeField()
    date_entrance = models.DateField()
    costumers_number = models.IntegerField(default=0)

