from django import forms
from django.contrib.auth.forms import UserCreationForm

from accounts.models import CustomUser


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ["username", "email", "password1", "password2"]
