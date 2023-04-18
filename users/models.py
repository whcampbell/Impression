from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import date

class CustomUser(AbstractUser) :

    artist_since = models.DateField(default=date.today())

    def __str__(self) :
        return self.username


# Create your models here.
