from datetime import date

from django.shortcuts import render, redirect
from Restaurant.models import RestaurantReservation


# Create your views here.


def restaurant_page(request):
    return render(request, 'restaurant/restaurant_page.html')
def restaurant_reservation_page(request):
    return render(request, 'restaurant/reservation_page.html')

def restaurant_validation_page(request):
    return render(request, 'restaurant/validated_list.html')

def reserved_tables(request):
    date_ = date.today()
    if request.method == 'POST':
        date_ = request.POST.get('fecha')
    booking = RestaurantReservation.objects.filter(date_entrance=date_)
    return render(request, 'restaurant/reserved_tables.html', {'reservas': booking})

def update_validation(request):
    if request.method == 'POST':
        reservation = RestaurantReservation.objects.get(id=request.POST.get('reserva_id'))
        reservation.validated = True
        reservation.save()
    return redirect('reserved_tables')
