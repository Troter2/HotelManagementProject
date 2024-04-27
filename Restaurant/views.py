from django.shortcuts import render
from Restaurant.models import RestaurantReservation


# Create your views here.


def restaurant_page(request):
    return render(request, 'restaurant/restaurant_page.html')
def restaurant_reservation_page(request):
    return render(request, 'restaurant/reservation_page.html')
