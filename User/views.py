from django.shortcuts import render, redirect
from django.urls import reverse
import datetime

from Reception.forms import ReservationForm
from Reception.models import RoomReservation
from Reception.views import validar_dni, validate_guests_phone
from User.forms import CustomerForm, ChangeProfileForm
from User.models import Customer
from django.contrib.auth.models import User


# Create your views here.
def add_guest_view(request, id):
    if request.user.has_perm('receptionist'):
        return render(request, 'user/add_guest.html', {"book_id": id})
    return redirect('home')


def save_more_guest(request, id):
    if request.user.has_perm('receptionist'):
        return render(request, 'user/add_guest.html', {"book_id": id})
    return redirect('home')


def save_guest(request, id):
    if request.user.has_perm('receptionist'):
        form = CustomerForm(request.POST)
        if form.is_valid():
            Customer.objects.create(reservation=RoomReservation.objects.get(id=id), name=request.POST['name'],
                                    lastname=request.POST['lastname'], DNI=request.POST['DNI'])
            return redirect('add_guest_view', id=id)
        return render(request, 'reception/reservedRooms.html')
    return redirect('home')


def user_profile(request):
    if request.user.is_authenticated:
        return render(request, 'user/profile.html')
    return redirect('home')


def user_edit_profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ChangeProfileForm(request.POST)
            if form.is_valid():
                request.user.first_name = request.POST['name']
                request.user.last_name = request.POST['lastname']
                request.user.email = request.POST['email']
                request.user.telefono = request.POST['phone']
                request.user.DNI = request.POST['DNI']
                request.user.username = request.POST['username']
                if not validar_dni(request.user.DNI):
                    form.add_error('DNI', 'El DNI no es válido.')
                if not validate_guests_phone(request.user.telefono):
                    form.add_error('guests_phone', 'El telefono introducido no es válido.')
                request.user.save()
                return redirect('user_profile')
        return render(request, 'user/edit_profile.html')
    return redirect('home')


def list_reservations_user(request):
    if request.user.is_authenticated:
        reserves = RoomReservation.objects.all().filter(DNI=request.user.DNI)
        context = {
            'reserves': reserves
        }
        return render(request, 'user/List_reserv_user.html', context)
    return redirect('home')


def booking_filter_user(request):
    if request.user.is_authenticated:
        fecha = request.POST['fecha']
        reserves_filtradas = RoomReservation.objects.all().filter(DNI=request.user.DNI)
        if fecha:
            reserves_filtradas = reserves_filtradas.filter(guest_checkin=fecha)
        return render(request, 'user/List_reserv_user.html', {'reserves': reserves_filtradas})
    return redirect('home')

def delete_booking_user(request):
    if request.user.is_authenticated:
        borrar_reserva = request.POST['id']
        reservation = RoomReservation.objects.get(pk=borrar_reserva)
        reservation.delete()
        return redirect(list_reservations_user)
    return redirect('home')
