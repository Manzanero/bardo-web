from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Campaign(models.Model):
    campaign_id = models.SlugField(max_length=256, unique=True, null=True)
    name = models.CharField(max_length=256, unique=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class CampaignProperty(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, default=None)
    name = models.CharField(max_length=256)
    value = models.CharField(max_length=256)

    class Meta:
        unique_together = ('campaign', 'user', 'name')


class Map(models.Model):
    map_id = models.SlugField(max_length=256, unique=True, null=True)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    data = models.TextField(default='{}')
    saved = models.DateTimeField(null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('campaign', 'map_id')


class MapProperty(models.Model):
    map = models.ForeignKey(Map, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, default=None)
    name = models.SlugField(max_length=256)
    value = models.CharField(max_length=256)

    class Meta:
        unique_together = ('map', 'user', 'name')


class Action(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, null=True)
    map = models.ForeignKey(Map, on_delete=models.CASCADE, null=True, default=None)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    data = models.TextField(default='{"name": null}')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {timezone.localtime(self.created).isoformat(timespec='microseconds')}"
