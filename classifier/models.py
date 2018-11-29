from django.db import models
from sorl.thumbnail import ImageField, get_thumbnail # Tool for image resizing before storage

# Create your models here.

class Item(models.Model):
    image = ImageField(upload_to='images/')
    summary = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        if self.image:
            self.image = get_thumbnail(self.image, '500x600', quality=99, format='JPEG').url
        super(Item, self).save(*args, **kwargs)

class User(models.Model):
    username = models.CharField(max_length=255)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=255)