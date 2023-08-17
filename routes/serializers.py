from events.serializers import EventReadSerializer
from routes.models import Route, CustomRoute
from rest_framework import serializers


class CustomRouteSerializer(serializers.ModelSerializer):
    waypoints = EventReadSerializer(many=True, required=False)

    class Meta:
        model = CustomRoute
        fields = ('id', 'user', 'duration', 'distance', 'waypoints')


class RouteSerializer(serializers.ModelSerializer):
    waypoints = EventReadSerializer(many=True, required=False)

    class Meta:
        model = Route
        fields = ('id', 'name', 'duration', 'distance', 'waypoints')