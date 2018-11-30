from django.db import models
from django_resized import ResizedImageField

# Create your models here.

class Item(models.Model):
    image = ResizedImageField(upload_to='images/')
    summary = models.CharField(max_length=255)


class User(models.Model):
    username = models.CharField(max_length=255)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=255)