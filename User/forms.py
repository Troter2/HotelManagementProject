from django import forms

from User.models import Customer


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['DNI', 'name', 'lastname']


class ChangeProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['DNI', 'name', 'lastname', 'email', 'phone',
                  'username']
