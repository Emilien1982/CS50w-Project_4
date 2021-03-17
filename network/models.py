from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.ManyToManyField("self", related_name="followerz", symmetrical=False)

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    text = models.CharField(max_length=280)
    time_creation = models.DateTimeField(auto_now_add=True)
    time_last_update = models.DateTimeField(null=True)
    likes = models.ManyToManyField(User, related_name="liker", symmetrical=False, null=True)
    