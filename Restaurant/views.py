from django.shortcuts import render
from Restaurant.models import RestaurantReservation


# Create your views here.

def restaurant_reservation_page(request):
    reservation = RestaurantReservation.objects.all()
    return render(request, 'Restaurant/reservations.html', {'reservations': reservation})


def restaurant_page(request):
    return render(request, 'restaurant/restaurant_page.html')
