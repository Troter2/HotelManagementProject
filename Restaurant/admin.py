from django.contrib import admin

from Restaurant.models import RestaurantReservation, Order, ItemAmount, Item

# Register your models here.

admin.site.register(RestaurantReservation)
admin.site.register(ItemAmount)
admin.site.register(Item)
admin.site.register(Order)