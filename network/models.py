from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields import DateTimeField, IntegerField, TextField
from django.db.models.fields.related import ForeignKey, ManyToManyField
from django.http import request


class User(AbstractUser):

    follower = models.ManyToManyField(
        'self', blank=True, related_name="followee")
    following = models.ManyToManyField(
        'self', blank=True, related_name="+")

    def follow_count(self):

        return{
            "follower": self.follower.all().count(),
            "following": self.following.all().count()
        }

    def follower_check(self, user, follow):

        item = User.objects.get(username=user)
        return True if item.follower.filter(username=follow) else False

    def following_check(self, user, following):

        item = User.objects.get(username=user)
        return True if item.following.filter(username=following) else False
    pass


class Post(models.Model):

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="creator")
    post = models.TextField()
    date = models.DateTimeField(auto_now=True)
    like = models.ManyToManyField(User, blank=True, related_name="like_count")

    def serialize(self, user_name):

        return {
            "user": self.user.username,
            "post": self.post,
            "date": self.date.strftime("%H:%M, on %d/%m/%Y"),
            "like": self.like.all().count(),
            "check_like": True if self.like.all().filter(username=user_name) else False
        }

    def like_count(self):

        return self.like.all().count()

    def check_like(self, username):
        item = self.like.all().filter(username=username)
        return True if item else False


class Comment(models.Model):

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="commentor")
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="content")
    comment = models.TextField()
    date = models.DateTimeField(auto_now=True)


class Follow(models.Model):

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="follow_ee")
    followee = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="follow_er")
