from django.http import HttpResponse
from django.shortcuts import render

from Reception.models import RoomReservation
from Restaurant.forms import RestaurantReservationForm


# Create your views here.


def restaurant_page(request):
    return render(request, 'restaurant/restaurant_page.html')


def restaurant_reservation_page(request):
    return render(request, 'restaurant/reservation_page.html')


def restaurant_reservation_page_uuid(request, uuid):
    initial_data = {}
    try:
        # Obtener la reserva de habitación asociada con el UUID
        room_reservation = RoomReservation.objects.get(reservation_number=uuid)
        initial_data = {
            'client_name': room_reservation.guests_name + ' ' + room_reservation.guests_surname,
            'room_reservation': room_reservation,
        }
    except RoomReservation.DoesNotExist:
        return HttpResponse("Reserva no encontrada")

    if request.method == 'POST':
        form = RestaurantReservationForm(request.POST)
        if form.is_valid():
            restaurant_reservation = form.save(commit=False)
            restaurant_reservation.room_reservation = room_reservation
            restaurant_reservation.save()
            return render(request, 'restaurant/thank_you.html')
        else:
            print(form.errors)

    return render(request, 'restaurant/autoreservation_page.html', {'data': initial_data})
