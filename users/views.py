from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from routes.serializers import RouteSerializer
from users.models import Role
from users.serializers import CustomUserSerializer


class RoleAPIListView(generics.ListAPIView):
    queryset = Role.objects.all()
    serializer_class = RouteSerializer