from django.contrib import admin

from Restaurant.models import RestaurantReservation, Dish

# Register your models here.

admin.site.register(RestaurantReservation)
admin.site.register(Dish)
