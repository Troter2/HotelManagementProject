from django.shortcuts import render, redirect, get_object_or_404

from Billing.forms import PromotionForm, CouponForm
from Billing.models import Promotion, Coupon
from Reception.models import RoomReservation
from Restaurant.models import RestaurantReservation


# Create your views here.
def list_offers(request):
    if request.user.has_perm('accountant'):
        promotions = Promotion.objects.all()
        coupons = Coupon.objects.all()
        return render(request, 'billing/list_offers.html', {'ofertas': promotions, 'cupones': coupons})
    return redirect('home')


def list_coupons(request):
    if request.user.has_perm('accountant'):
        coupons = Coupon.objects.all()
        return render(request, 'billing/list_coupons.html', {'cupones': coupons})
    return redirect('home')


def edit_status_coupon(request):
    if request.user.has_perm('accountant') and request.method == 'POST':
        coupon_id = request.POST['id_coupon']
        coupon = get_object_or_404(Coupon, pk=coupon_id)
        if coupon.active == True:
            coupon.active = False
        else:
            coupon.active = True
        coupon.save()
        return redirect('list_coupons')
    return redirect('home')


def create_coupon(request):
    if request.user.has_perm('accountant') and request.method == 'POST':
        form = CouponForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('list_coupons')
    return redirect('home')


def edit_coupon(request):
    if request.user.has_perm('accountant') and request.method == 'POST':
        coupon_id = request.POST['id']
        coupon = get_object_or_404(Coupon, pk=coupon_id)
        coupon.discount_percentage = request.POST['discount_percentage']
        coupon.discount_code = request.POST['discount_code']
        coupon.save()
        return redirect('list_coupons')
    return redirect('home')


def create_offer(request):
    if request.user.has_perm('accountant') and request.method == 'POST':
        form = PromotionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('list_offers')
    return redirect('home')


def list_restaurant_and_room(request):
    if request.user.has_perm('accountant'):
        reservations = RoomReservation.objects.filter(guest_leaved=True)
        return render(request, 'billing/list_reservations.html', {'reservas': reservations})


def edit_offer(request):
    if request.user.has_perm('accountant'):
        offer = Promotion.objects.get(pk=request.POST['id'])
        if 'image' in request.FILES:
            offer.image = request.FILES['image']
        offer.title = request.POST['title']
        offer.description = request.POST['description']
        offer.save()
        return redirect('list_offers')
    return redirect('home')


def delete_offer(request, offer_id):
    if request.method == 'POST' and request.user.has_perm('accountant'):
        promotion = get_object_or_404(Promotion, id=offer_id)
        coupon = promotion.discount_code
        coupon.active = False
        coupon.save()
        promotion.delete()
        return redirect('list_offers')
    return redirect('home')


def details_reservation(request, reservation_id):
    room_reservation = get_object_or_404(RoomReservation, pk=reservation_id)
    restaurant_reservations = RestaurantReservation.objects.filter(room_reservation=room_reservation)
    return render(request, 'billing/details_reservation.html',
                  {'room_reservation': room_reservation, 'restaurant_reservations': restaurant_reservations})
