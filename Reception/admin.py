from django.contrib import admin

from Reception.models import RoomReservation

# Register your models here.

admin.site.register(RoomReservation)

from Reception.models import Room, RoomType

# Register your models here.
admin.site.register(Room)
admin.site.register(RoomType)
