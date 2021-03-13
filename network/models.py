from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.ManyToManyField("self", symmetrical=False, related_name="followerz")

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    text = models.CharField(max_length=280)
    time_creation = models.DateTimeField(auto_now_add=True)
    time_last_update = models.DateTimeField(auto_now=True)
    likes = models.ForeignKey(User, on_delete=models.CASCADE, related_name="liker", null=True, unique=True)