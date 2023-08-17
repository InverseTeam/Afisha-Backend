from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from users.models import Role
from users.serializers import RoleSerializer


class RoleAPIListView(generics.ListAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer