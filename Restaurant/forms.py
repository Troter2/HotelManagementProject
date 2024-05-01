from django import forms
from .models import RestaurantReservation, Item


class RestaurantReservationForm(forms.ModelForm):
    class Meta:
        model = RestaurantReservation
        fields = ['client_name', 'entrance_hours', 'date_entrance', 'costumers_number']
        exclude = ['room_reservation']

    def __init__(self, *args, **kwargs):
        super(RestaurantReservationForm, self).__init__(*args, **kwargs)
        self.fields['client_name'].widget.attrs['readonly'] = True


class RestaurantBookingForm(forms.ModelForm):
    class Meta:
        model = RestaurantReservation
        fields = ['client_name', 'entrance_hours', 'date_entrance', 'costumers_number']



class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'price', 'img']

class ItemFormWithoutImg(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'price']