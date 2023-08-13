import json
import random
import requests
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from routes.models import Route


class RouteSerializer(serializers.ModelSerializer):
    cover = serializers.ImageField(required=False)
    waypoints = serializers.JSONField(required=False)
    
    class Meta:
        model = Route
        fields = ('id', 'name', 'cover', 'tickets', 'waypoints')