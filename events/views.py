from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from events.models import Event, Platform, Category, Tag
from events.serializers import CommentSerializer, EventSerializer, PlatformSerializer, CategorySerializer, TagSerializer
from users.models import CustomUser
from users.permissions import IsManager


class EventAPIListCreate(generics.ListCreateAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsManager]

    def get_queryset(self):
        return Event.objects.filter(open=True)


class EventAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsManager]


class EventAPIPLatformListView(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Event.objects.filter(platform=self.kwargs['pk'])
    

class EventAPICategoryListView(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Event.objects.filter(category=self.kwargs['pk'])
    

class EventAPITagListView(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Event.objects.filter(tags__id=self.kwargs['pk'])
    

class EventAPITicketBuyView(generics.UpdateAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        obj = Event.objects.get(pk=self.kwargs['pk'])
        customer = self.request.user

        customer.money -= obj.price

        obj.tickets.add(customer.pk)
        obj.save()
        customer.save()

        serializer = EventSerializer(obj, required=False)

        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)
    

class EventAPIMyTicketsView(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.events_user.all()


class PlatformAPIListView(generics.ListAPIView):
    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer
    permission_classes = [IsAuthenticated]


class CategoryAPIListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]


class TagAPIListView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]


class CommentAPICreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            event = Event.objects.get(pk=self.kwargs['pk'])
            event.comments.add(serializer.data['id'])
            event.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)