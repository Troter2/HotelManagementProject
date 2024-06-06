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


class AdminRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match")

        return cleaned_data

    def save(self, commit=True):
        user = super(AdminRegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user