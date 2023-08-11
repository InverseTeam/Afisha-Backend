import json
import random
import requests
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from routes.models import Route, RouteType


class RouteTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteType
        fields = ('id', 'name', 'query_text')


class RouteReadSerializer(serializers.ModelSerializer):
    cover = serializers.ImageField(required=False)
    route_type = RouteTypeSerializer(required=False)
    waypoints = serializers.JSONField(required=False)
    
    class Meta:
        model = Route
        fields = ('id', 'name', 'cover', 'duration', 'start_date', 'end_date', 'price', 'route_type', 'active', 'waypoints')


class RouteWriteSerializer(serializers.ModelSerializer):
    cover = serializers.ImageField(required=False)
    waypoints = serializers.JSONField(required=False)
    
    class Meta:
        model = Route
        fields = ('id', 'name', 'cover', 'duration', 'start_date', 'end_date', 'price', 'route_type', 'active', 'waypoints')


