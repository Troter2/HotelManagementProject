from django.shortcuts import render
from Restaurant.models import RestaurantReservation

# Create your views here.

def restaurant_reservation_page(request):
    reservation = RestaurantReservation.objects.all()
    return render(request, 'Restaurant/reservations.html', {'reservations': reservation})
