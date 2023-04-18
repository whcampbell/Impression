from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class CustomUser(AbstractUser) :

    artist_since = models.DateField(default=timezone.now)

    def __str__(self) :
        return self.username


# Create your models here.
