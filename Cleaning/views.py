import datetime

from django.utils import timezone

from Reception.models import Room, RoomReservation
from django.shortcuts import render, redirect


# Create your views here.



def cleaner_page(request):
    rooms = Room.objects.all()
    reservations = RoomReservation.objects.filter(guest_checkout=datetime.date.today())
    last_rooms = []
    last_rooms_id=[]
    for reservation in reservations:
        last_rooms.append(reservation.room_number)
        last_rooms_id.append(reservation.room_number.id)
    first_room = Room.objects.all().filter(is_clean=False).exclude(id__in=last_rooms_id)
    rooms=list(first_room) + last_rooms
    return render(request, 'cleaner/cleaner_page.html', {'rooms': rooms})


def update_room_status(request):
    if request.method == 'POST':
        room_id = request.POST.get('room_id')
        action = request.POST.get('action')
        room = Room.objects.get(pk=room_id)
        room.is_clean = (action == 'clean')
        room.save()
    return redirect('cleaner_page')
