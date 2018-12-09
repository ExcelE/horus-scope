from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class CustomUser(AbstractUser):
    # name = models.CharField(max_length=100, null=True)
    # email = models.EmailField(null=True)
    tokens = models.IntegerField(default=10)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.username

class Classification(models.Model):
    # The related_name is the name that settings.AUTH_USER_MODEL will use for RelatedFields
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='classifications')
    name = models.CharField(max_length=100)
    probability = models.FloatField()
    summary = models.TextField()

    def __str__(self):
        return self.name

