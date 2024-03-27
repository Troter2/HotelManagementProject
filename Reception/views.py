import datetime

from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template

from Reception.models import RoomReservation


# Create your views here.
class Room(object):
    def __init__(self, number, is_clean):
        self.number = number
        self.is_clean = is_clean


def receptionIni(request):
    test = "hello world"
    cur_date = datetime.datetime.now()
    rooms = [Room(103, True), Room(104, True), Room(105, True), Room(106, True), Room(107, True)]

    return render(request, 'reception/home.html',
                  ({"test": test, "test2": "i'm here", "cur_date": cur_date, "rooms": rooms}))


def roomView(request):
    habitacions = RoomReservation.objects.all()
    context = {
        'habitacions': habitacions
    }
    return render(request, 'reception/roomsType.html', context)


def reservedRoomsView(request):
    reserves = RoomReservation.objects.all()
    context = {
        'reserves': reserves
    }
    return render(request, 'reception/reservedRooms.html', context)
