from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from users.models import Artist
from users.serializers import ArtistSerializer
from users.permissions import IsArtistManager, IsManager


class ArtistAPIListCreateView(generics.ListCreateAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = [IsManager]


class ArtistsAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = [IsArtistManager]


class ArtistsAPIMyListView(generics.ListAPIView):
    serializer_class = ArtistSerializer
    permission_classes = [IsManager]

    def get_queryset(self):
        return Artist.objects.filter(manager=self.request.user.id)