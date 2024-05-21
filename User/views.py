from django.shortcuts import render, redirect
from django.urls import reverse
import datetime
from Reception.models import RoomReservation
from User.forms import CustomerForm
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
