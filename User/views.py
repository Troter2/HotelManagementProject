from django.shortcuts import render, redirect
from User.models import Shift
from Reception.models import RoomReservation
from User.forms import CustomerForm
from User.models import Customer


# Create your views here.

def shift_management_page(request):
    users = Shift.objects.all()
    return render(request, 'personal_manager/shift_management_page.html', {'users': users})


# Create your views here.
def add_guest_view(request, id):
    return render(request, 'user/add_guest.html',{"book_id": id})


def save_more_guest(request, id):
    return render(request, 'user/add_guest.html',{"book_id": id})


def save_guest(request,id):
    form = CustomerForm(request.POST)
    if form.is_valid():
        Customer.objects.create(reservation=RoomReservation.objects.get(id=id), name=request.POST['name'], lastname=request.POST['lastname'], DNI=request.POST['DNI'])
        return redirect('add_guest_view', id=id)
    return render(request, 'reception/reservedRooms.html')

