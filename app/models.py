from django.db import models
from django.contrib.auth.models import User
import os


def content_album_name(instance, filename):
    return os.path.join(instance.user.username, filename)


class AppFbUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField("Name", max_length=64)
    profile_url = models.CharField("Profile Picture Url", max_length=128)
    profile_pic = models.ImageField("Profile Picture", upload_to=content_album_name, blank=False)

    def __str__(self):
        return self.user.username
