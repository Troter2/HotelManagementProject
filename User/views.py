from django.shortcuts import render, redirect
from django.urls import reverse
import datetime

from Reception.forms import ReservationForm
from Reception.models import RoomReservation
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
                request.user.save()
                return redirect('user_profile')
        return render(request, 'user/edit_profile.html')
    return redirect('home')
