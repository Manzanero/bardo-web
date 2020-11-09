from django.db import models


class Campaign(models.Model):
    name = models.SlugField(max_length=256)
    data = models.TextField(default='{"name": null}')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Map(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    name = models.SlugField(max_length=256)
    data = models.TextField(default='{"name": null}')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Action(models.Model):
    map = models.ForeignKey(Map, on_delete=models.CASCADE)
    name = models.SlugField(max_length=256)
    data = models.TextField(default='{"name": null}')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
