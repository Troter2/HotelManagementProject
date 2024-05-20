from django.shortcuts import render, redirect
from django.urls import reverse
import datetime
from User.models import Shift
from Reception.models import RoomReservation
from User.forms import CustomerForm
from User.models import Customer
from django.contrib.auth.models import User


# Create your views here.

def shift_management_page(request):
    users = User.objects.all()
    return render(request, 'personal_manager/shift_management_page.html', {'users': users})


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


def previous_week(request):
    if request.user.has_perm('receptionist'):
        current_date = datetime.datetime.now()
        start_of_previous_week = current_date - datetime.timedelta(days=current_date.weekday(), weeks=1)
        return redirect(reverse('shift_management_page'))
    return redirect('home')


def next_week(request):
    if request.user.has_perm('receptionist'):
        current_date = datetime.datetime.now()
        start_of_next_week = current_date + datetime.timedelta(days=(7 - current_date.weekday()))
        return redirect(reverse('shift_management_page'))
    return redirect('home')
