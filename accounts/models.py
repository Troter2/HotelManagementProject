from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    DNI = models.CharField(max_length=9)
    telefono = models.CharField(max_length=11)
