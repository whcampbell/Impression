from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

# create the file path for a user's media upload
def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    if (type(instance) == BlogPost) :
        return "user_{0}/{1}".format(instance.user.username, filename)
    return "user_{0}/{1}".format(instance.username, filename)

# Custom data model for a site user
# adds a friend list, header photo, and the date they became an artist
class CustomUser(AbstractUser) :

    description = models.TextField(default="I am an artist.")
    friends = models.ManyToManyField('self', blank=True)
    artist_since = models.DateField(default=timezone.now)
    main_photo = models.ImageField(upload_to=user_directory_path, default='no_image')

    def __str__(self) :
        return self.username

# Model for a blog post written by an associated user
# the (less obvious) alt_text field is for the <img> alt text attribute
class BlogPost(models.Model) :
    title = models.CharField(default="My Post", max_length=128)
    body = models.TextField(default="The World is Violet")
    image = models.ImageField(upload_to=user_directory_path, default="no_image")
    alt_text = models.CharField(default="Blog Post Picture", max_length=256)
    post_date = models.DateTimeField(default = timezone.now)
    user = models.ForeignKey("CustomUser", on_delete=models.CASCADE)

    class Meta:
        # first post drawn is the most recent one
        ordering=["-post_date"]

# Model for a message sent between two users
# is_friend_request good for internal logic - they can't
# send messages to non-friends, so this is done via link on profile page
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
    is_friend_request = models.BooleanField(default=False)

    class Meta:
        ordering = ['-time_sent']

    def __str__(self) :
        return self.title