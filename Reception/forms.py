from django import forms
from .models import RoomReservation

class ReservationForm(forms.ModelForm):
    class Meta:
        model = RoomReservation
        fields = ['guests_name', 'guests_surname', 'DNI', 'guests_email', 'guests_phone', 'guests_number']