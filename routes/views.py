from routes.serializers import *
from routes.models import *
from users.permissions import IsManagerOrAdminOrReadOnly
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class RouteAPIListCreateView(generics.ListCreateAPIView):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = [IsManagerOrAdminOrReadOnly]


class RouteAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = [IsManagerOrAdminOrReadOnly]


class CustomRouteAPIListCreateView(generics.ListCreateAPIView):
    queryset = Route.objects.all()
    serializer_class = CustomRouteSerializer
    permission_classes = [IsAuthenticated]


class CustomRouteAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Route.objects.all()
    serializer_class = CustomRouteSerializer
    permission_classes = [IsAuthenticated]
