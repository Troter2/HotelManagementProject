import datetime

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.loader import get_template
from Reception.models import RoomReservation, RoomType
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


def rooms_view(request):
    rooms = RoomType.objects.all()
    context = {
        'rooms': rooms
    }
    return render(request, 'reception/roomsType.html', context)


def update_book_arrive(request):
    if request.method == 'POST':
        reservation = RoomReservation.objects.get(id=request.POST.get('id'))
        reservation.guest_is_here = True
        reservation.save()
    return redirect('reserved_rooms_view')


def update_book_gone(request):
    if request.method == 'POST':
        reservation = RoomReservation.objects.get(id=request.POST.get('id'))
        reservation.guest_is_here = True
        reservation.save()
    return redirect('reserved_rooms_view')


def reserved_rooms_view(request):
    reserves = RoomReservation.objects.all().filter(guest_is_here=False)
    context = {
        'reserves': reserves
    }
    return render(request, 'reception/reservedRooms.html', context)


def ocuped_rooms_view(request):
    reserves = RoomReservation.objects.all().filter(guest_is_here=False)
    context = {
        'reserves': reserves
    }
    return render(request, 'reception/ocuped_rooms.html', context)


def pay_reservation(request):
    if request.method == 'POST':
        reserva_id = request.POST.get('id')
        reserva = RoomReservation.objects.get(pk=reserva_id)
        reserva.room_is_payed = True
        reserva.save()
    return redirect('reserved_rooms_view2')


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
        if form.is_valid():
            dni = form.cleaned_data['DNI']
            guest_name = form.cleaned_data['guest_name']
            guest_checkin = form.cleaned_data['guest_checkin']
            guest_surname = form.cleaned_data['guest_surname']
            if not validar_dni(dni):
                form.add_error('DNI', 'El DNI no es válido.')
            existing_reservation = RoomReservation.objects.filter(DNI=dni).first()
            if existing_reservation:
                existing_reservation.guest_checkin = guest_checkin
                existing_reservation.save()
            else:
                # Si no existeix el DNI en la BBDD
                form.add_error('DNI', 'El DNI no se ha encontrado en la base de datos')

            return redirect('reception/thank_you.html')
        else:
            form = CheckIn()
    else:
        form = CheckIn()
    return render(request, 'reception/checkIn.html', {'form': form})
