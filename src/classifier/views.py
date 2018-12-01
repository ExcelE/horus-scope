from django.shortcuts import render
from django.contrib import auth
from .models import Item, User, Prediction
from rest_framework import viewsets

from .serializers import ItemSerializer, UserSerializer, PredictionSerializer

# Create your views here.

class ItemView(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class PredictionView(viewsets.ModelViewSet):
    queryset = Prediction.objects.all()
    serializer_class = PredictionSerializer