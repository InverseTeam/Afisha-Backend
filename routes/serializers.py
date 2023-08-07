from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from routes.models import Route, RouteType


class RouteTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteType
        fields = ('id', 'name')


class RouteSerializer(serializers.ModelSerializer):
    cover = Base64ImageField(represent_in_base64=True, required=False)
    route_type = RouteTypeSerializer(required=False)
    waypoints = serializers.JSONField()
    
    class Meta:
        model = Route
        fields = ('id', 'name', 'cover', 'duration', 'start_date', 'end_date', 'price', 'route_type', 'active', 'waypoints')


