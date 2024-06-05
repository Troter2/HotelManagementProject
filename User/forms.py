from django import forms
from django.contrib.auth.models import Group

from Reception.models import CustomUser
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

from django import forms

class UserGroupForm(forms.ModelForm):
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = CustomUser
        fields = ['groups']
