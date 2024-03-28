import datetime

from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from Reception.models import RoomReservation
from Reception.forms import ReservationForm, CheckIn


# Create your views here.
class Room(object):
    def __init__(self, number, is_clean):
        self.number = number
        self.is_clean = is_clean


def reception_ini(request):
    test = "hello world"
    cur_date = datetime.datetime.now()
    rooms = [Room(103, True), Room(104, True), Room(105, True), Room(106, True), Room(107, True)]

    return render(request, 'reception/home.html',
                  ({"test": test, "test2": "i'm here", "cur_date": cur_date, "rooms": rooms}))


def room_view(request):
    habitacions = RoomReservation.objects.all()
    context = {
        'habitacions': habitacions
    }
    return render(request, 'reception/roomsType.html', context)


def reserved_rooms_view(request):
    reserves = RoomReservation.objects.all()
    context = {
        'reserves': reserves
    }
    return render(request, 'reception/reservedRooms.html', context)


def book_room(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            dni = form.cleaned_data['DNI']
            if not validar_dni(dni):
                form.add_error('DNI', 'El DNI no es válido.')
                return render(request, 'reception/reserve_room.html', {'form': form})
            return render(request, 'reception/thank_you.html')
    else:
        form = ReservationForm()
    return render(request, 'reception/reserve_room.html', {'form': form})


def validar_dni(dni):
    if len(dni) != 9:
        return False
    if not dni[:8].isdigit():
        return False
    if not dni[8].isalpha():
        return False
    return True

def checkin_form(request):
    if request.method == 'POST':
        form = CheckIn(request.POST)
        # if form.is_valid():
            # form.save()
            # return redirect('success_url')  Reemplaza 'success_url' con la URL de tu página de éxito
    else:
        form = CheckIn()
    return render(request, 'reception/checkIn.html', {'form': form})
