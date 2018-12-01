from rest_framework import serializers
from .models import Item, User, Prediction

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id', 'image', 'created_at', 'user')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'name', 'email', 'tokens', 'password', 'created_at', 'updated_at')

class PredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prediction
        fields = ('id', 'name', 'probability', 'summary', 'item')