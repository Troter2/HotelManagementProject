from django.contrib import admin

from Reception.models import RoomReservation
from Reception.models import Room, RoomType
from Restaurant.models import RestaurantReservation_v2

# Register your models here.


admin.site.register(RoomReservation)
admin.site.register(Room)
admin.site.register(RoomType)
admin.site.register(RestaurantReservation_v2)