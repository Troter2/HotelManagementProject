from django import forms
from .models import RoomReservation


class ReservationForm(forms.ModelForm):
    class Meta:
        model = RoomReservation
        fields = ['DNI', 'guests_name', 'guests_surname', 'guests_email', 'guests_phone',
                 'guest_checkin', 'guest_checkout', 'guests_number']


class CheckIn(forms.ModelForm):
    class Meta:
        model = RoomReservation
        fields = ['DNI', 'guests_name', 'guests_surname', 'guest_checkin']
