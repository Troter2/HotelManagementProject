from django.utils import timezone

from Reception.models import Room, RoomReservation
from django.shortcuts import render, redirect


# Create your views here.

def cleaner_shift(request):
    room = Room.objects.all()
    return render(request, 'shifts/shift.html', {'room': room})


def cleaner_page(request):
    rooms = Room.objects.all()
    return render(request, 'cleaner/cleaner_page.html', {'rooms': rooms})


def update_room_status(request):
    if request.method == 'POST':
        room_id = request.POST.get('room_id')
        action = request.POST.get('action')
        room = Room.objects.get(pk=room_id)
        room.is_clean = (action == 'clean')
        room.save()
    return redirect('cleaner_page')
