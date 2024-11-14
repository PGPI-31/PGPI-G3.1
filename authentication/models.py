from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    telephone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    dni = models.CharField(max_length=10, blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)