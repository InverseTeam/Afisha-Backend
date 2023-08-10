from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from users.serializers import CustomUserSerializer
from users.permissions import IsArtistManager, IsManager
