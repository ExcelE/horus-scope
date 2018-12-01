from django.db import models
from django_resized import ResizedImageField

# Create your models here.

class Item(models.Model):
    image = ResizedImageField(upload_to='images/')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        null=True 
    )

class Prediction(models.Model):
    name = models.CharField(max_length=100)
    probability = models.FloatField()
    summary = models.TextField()
    item = models.ForeignKey(
        'Item',
        on_delete=models.CASCADE,
        null=True 
    )

class User(models.Model):
    username = models.CharField(max_length=255)
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(null=True)
    password = models.CharField(max_length=512)
    tokens = models.IntegerField(default=10)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.email
    
    def tokens(self):
        return self.tokens
