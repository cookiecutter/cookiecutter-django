from django.db import models


class Fruit(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1024)
    detail = models.TextField()
    detail_link = models.URLField(max_length=512)
