from django.db import models


# Create your models here.


class Shift(models.Model):
    user = models.CharField(max_length=16)
    password = models.CharField(max_length=50)
    shift = models.DateTimeField()
