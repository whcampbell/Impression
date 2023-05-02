from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return "user_{0}/{1}".format(instance.username, filename)

class CustomUser(AbstractUser) :

    artist_since = models.DateField(default=timezone.now)
    main_photo = models.ImageField(upload_to=user_directory_path, default='no_image')

    def __str__(self) :
        return self.username

class SliderImage() :
    image = models.ImageField(upload_to=user_directory_path)
    user = models.ForeignKey("CustomUser", on_delete=models.CASCADE)


# Create your models here.
