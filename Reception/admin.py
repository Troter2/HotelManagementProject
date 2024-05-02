from django.contrib import admin

from Reception.models import RoomReservation
from Reception.models import Room, RoomType

# Register your models here.


admin.site.register(RoomReservation)
admin.site.register(Room)
admin.site.register(RoomType)
admin.site.register(LostItem)
