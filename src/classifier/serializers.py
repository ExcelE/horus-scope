from rest_framework import serializers
from .models import Classification, CustomUser
from rest_framework.validators import UniqueValidator

import logging
import sys
logger = logging.getLogger(__name__)


class UserSerializer(serializers.ModelSerializer):
    # classifications is aptly named from models.Classification's related_name
    classifications = serializers.PrimaryKeyRelatedField(many=True, queryset=Classification.objects.all(), allow_null=True, default=None)
    username = serializers.CharField(validators=[UniqueValidator(queryset=CustomUser.objects.all())])
    password = serializers.CharField(write_only=True)

    # create must be specifically defined for create_user to be overridden since the default is objects.create()
    def create(self, validated_data):
        # The first positional argument is always the username - everything else are keyword arguments
        user = CustomUser.objects.create_user(validated_data['username'], password=validated_data['password'])
        return user

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'password', 'tokens', 'created_at', 'updated_at', 'classifications')

class ClassificationSerializer(serializers.ModelSerializer):
    # "owner" in the source is a serializer property, defined in views.ClassificationList.perform_create arguments
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Classification
        fields = ('id', 'name', 'probability', 'summary', 'owner')


