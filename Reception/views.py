import datetime
from datetime import datetime
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from Reception.models import RoomReservation, RoomType, Room
from Reception.forms import ReservationForm, CheckIn


def reception_ini(request):
    return render(request, 'reception/home.html')


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


def habitaciones_libres(guest_entry, guest_leave):
    reservas_ocupadas = RoomReservation.objects.filter(
        Q(guest_checkin__lte=guest_entry, guest_checkout__gte=guest_entry) |
        Q(guest_checkin__lte=guest_leave, guest_checkout__gte=guest_leave) |
        Q(guest_checkin__gte=guest_entry, guest_checkout__lte=guest_leave)
    ).values_list('room_number_id', flat=True)

    habitaciones_libres = Room.objects.exclude(id__in=reservas_ocupadas)

    return habitaciones_libres


def reserve_room(request):
    roomTypes = RoomType.objects.all()
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            dni = form.cleaned_data['DNI']
            if not validar_dni(dni):
                form.add_error('DNI', 'El DNI no es válido.')
                return render(request, 'reception/reserve_room.html', {'form': form, 'roomTypes': roomTypes})
            form.instance.price = 60
            uuid = 1
            nights = (datetime.strptime(request.POST['guest_checkout'], '%Y-%m-%d') - datetime.strptime(
                request.POST['guest_checkin'], '%Y-%m-%d')).days
            free_rooms = habitaciones_libres(datetime.strptime(request.POST['guest_checkin'], '%Y-%m-%d'),
                                             datetime.strptime(request.POST['guest_checkout'], '%Y-%m-%d'))
            if len(free_rooms) < 1:
                return render(request, 'reception/reservation_form.html', {'form': form, 'roomTypes': roomTypes})

            RoomReservation.objects.create(reservation_number=uuid, DNI=request.POST['DNI'],
                                           guests_name=request.POST['guests_name'],
                                           guests_surname=request.POST['guests_surname'],
                                           guests_email=request.POST['guests_email'],
                                           guests_phone=request.POST['guests_phone'],
                                           guest_checkin=request.POST['guest_checkin'],
                                           guest_checkout=request.POST['guest_checkout'],
                                           guests_number=request.POST['guests_number'],
                                           price=(RoomType.objects.filter(id=request.POST['room_type'])[
                                                      0].price + int(request.POST['guests_number'])) * nights,
                                           room_number=free_rooms[0]

                                           )
            return render(request, 'reception/thank_you.html')
    else:
        form = ReservationForm()
    return render(request, 'reception/reservation_form.html', {'form': form, 'roomTypes': roomTypes})


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
