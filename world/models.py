from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Campaign(models.Model):
    name = models.SlugField(max_length=256)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class CampaignProperty(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.SlugField(max_length=256)
    value = models.CharField(max_length=256)


class Map(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    name = models.SlugField(max_length=256)
    data = models.TextField(default='{}')
    saved = models.DateTimeField(null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Action(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, null=True)
    map = models.ForeignKey(Map, on_delete=models.CASCADE, null=True, default=None)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    data = models.TextField(default='{"name": null}')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + ' - ' + timezone.localtime(self.created).isoformat(timespec='microseconds')
