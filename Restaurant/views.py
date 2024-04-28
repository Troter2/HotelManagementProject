from datetime import date

from django.shortcuts import render, redirect
from Restaurant.models import RestaurantReservation, Order, ItemAmount


# Create your views here.


def restaurant_page(request):
    return render(request, 'restaurant/restaurant_page.html')


def restaurant_reservation_page(request):
    return render(request, 'restaurant/reservation_page.html')


def restaurant_validation_page(request):
    booking = RestaurantReservation.objects.filter(validated=True)
    return render(request, 'restaurant/validated_list.html', {'reservas': booking})


def reserved_tables(request):
    date_ = date.today()
    if request.method == 'POST':
        if request.POST.get('fecha') == "":
            pass
        else:
            date_ = request.POST.get('fecha')
    booking = RestaurantReservation.objects.filter(date_entrance=date_).filter(validated=False)
    return render(request, 'restaurant/reserved_tables.html', {'reservas': booking})


def update_validation(request):
    if request.method == 'POST':
        reservation = RestaurantReservation.objects.get(id=request.POST.get('reserva_id'))
        reservation.validated = True
        reservation.save()
    return redirect('reserved_tables')


def calculate_total(order):
    total = 0
    items = ItemAmount.objects.filter(order=order)
    for item in items:
        total += item.item.price * item.amount
    return total


def set_order(request):
    if request.method == 'POST':
        if request.POST.get('reservation_id') == "" or request.POST.get('order_number') == "":
            pass
        else:
            order = Order.objects.get(id=request.POST.get('order_number'))
            reservation = RestaurantReservation.objects.get(id=request.POST.get('reservation_id'))
            reservation.order_num = order
            order.total = calculate_total(order)
            order.save()
            reservation.save()
    return redirect("restaurant_validation_page")
