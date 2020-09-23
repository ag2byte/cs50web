from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime


class User(AbstractUser):
    pass


class Post(models.Model):
    # Model for a post
    content = models.CharField(max_length=144)
    author = models.ForeignKey(
        'User', related_name="all_posts", on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    last_edited_on = models.DateTimeField(auto_now=True)
    like = models.ManyToManyField(User, blank=True, related_name="liked_user")

    def __str__(self):
        return self.author.username


class Profile(models.Model):
    # Model for profile
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    follower = models.ManyToManyField(
        User,  blank=True, related_name="follower")
    following = models.ManyToManyField(
        User,  blank=True, related_name="following")

    def __str__(self):
        return self.user.username
