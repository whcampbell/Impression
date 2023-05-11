from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return "user_{0}/{1}".format(instance.username, filename)

class CustomUser(AbstractUser) :

    friends = models.ManyToManyField('self', blank=True)
    artist_since = models.DateField(default=timezone.now)
    main_photo = models.ImageField(upload_to=user_directory_path, default='no_image')

    def __str__(self) :
        return self.username

class SliderImage(models.Model) :
    image = models.ImageField(upload_to=user_directory_path)
    user = models.ForeignKey("CustomUser", on_delete=models.CASCADE)

class Message(models.Model) :
    sender = models.ForeignKey(
        "CustomUser", 
        on_delete=models.CASCADE,
        related_name="sent_messages"
    )
    receiver = models.ForeignKey(
        "CustomUser", 
        on_delete=models.CASCADE,
        related_name="received_messages"
    )
    time_sent = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=64, default="New Message")
    body = models.TextField()
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-time_sent']

    def __str__(self) :
        return self.title


# Create your models here.
