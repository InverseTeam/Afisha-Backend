import requests
from faker import Faker
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from events.models import *
from events.serializers import *
from events.parser import get_events
from users.models import CustomUser
from users.permissions import IsManager
from rest_framework.decorators import api_view
from django.core.files.base import ContentFile


class EventAPIListCreate(generics.ListCreateAPIView):
    serializer_class = EventReadSerializer
    permission_classes = [IsManager]

    def get(self, request):
        queryset = Event.objects.all()
        serializer = EventReadSerializer(queryset, many=True)
        
        return Response(serializer.data)

    def post(self, request):
        serializer = EventWriteSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        
        return Response(serializer.errors, status=400)

    def get_queryset(self):
        return Event.objects.filter(open=True)
    

class EventAPIMyListView(generics.ListAPIView):
    serializer_class = EventReadSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Event.objects.filter(artists__manager__pk=self.request.user.pk)
    

class EventAPIFilterListView(generics.ListAPIView):
    serializer_class = EventReadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        events = Event.objects
        desired_date = self.request.GET.get('date', None)
        category = self.request.GET.get('category', None)
        age_category = self.request.GET.get('age_category', None)
        open = self.request.GET.get('open', None)

        if desired_date: events = events.filter(start_date=desired_date)
        if category: events = events.filter(category=category)
        if age_category: events = events.filter(age_limit=age_category)
        if open: events = events.filter(published=open)

        return events


class EventAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventReadSerializer
    permission_classes = [IsManager]

    def get(self, request, pk):
        event = Event.objects.get(pk=pk)
        serializer = EventReadSerializer(event)
        
        return Response(serializer.data)

    def patch(self, request, pk):
        event = Event.objects.get(pk=pk)
        serializer = EventWriteSerializer(event, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            
            return Response(serializer.data, status=201)
        
        return Response(serializer.errors, status=400)
    

class EventAPICategoryListView(generics.ListAPIView):
    serializer_class = EventReadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Event.objects.filter(category=self.kwargs['pk'])
    

class EventAPITagListView(generics.ListAPIView):
    serializer_class = EventReadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Event.objects.filter(tags__id=self.kwargs['pk'])
    

class EventImageAPICreateView(generics.CreateAPIView):
    serializer_class = EventImageSerializer
    permission_classes = [IsManager]
    

class PlatformAPIListView(generics.ListAPIView):
    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer
    permission_classes = [IsAuthenticated]


class PlatformAPIDetailView(generics.RetrieveAPIView):
    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer
    permission_classes = [IsAuthenticated]


class CategoryAPIListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]


class CommentAPICreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            event = Event.objects.get(pk=self.kwargs['pk'])
            event.comments.add(serializer.data['id'])
            event.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TicketAPICreateView(generics.CreateAPIView):
    serializer_class = TicketWriteSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = TicketWriteSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            ticket = Ticket.objects.get(pk=serializer.data['id'])
            event = Event.objects.get(pk=self.kwargs['pk'])
            event.tickets.add()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        

class TicketAPIMyListView(generics.ListAPIView):
    serializer_class = TicketReadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Ticket.objects.filter(user=self.request.user.pk)
    
    
@api_view(['POST'])
def generate_events(request):
    if request.method == 'POST':
        events_data = get_events()
        fake = Faker()

        for event in events_data:
            new_event = Event(
                name=event['name'],
                start_date=fake.date_between(start_date='today', end_date='+12m'),
                description=event['description']
            )

            if event['age_category'] == '0+':
                new_event.age_category = Role.objects.get(pk=2)

            else:
                new_event.age_category = Role.objects.get(pk=1)

            if not Platform.objects.filter(name=event['platform']):
                platform = Platform(name=event['platform'], location=event['location'])
                platform.save()

            else:
                platform = Platform.objects.get(name=event['platform'])
                new_event.platform = platform

            image = requests.get(event['cover'])
            image_data = ContentFile(image.content)
            image_name = str(uuid.uuid4())
            new_event.cover.save(f'{image_name}.png', image_data, save=True)

            if not Category.objects.filter(name=event['name']):
                category = Category(name=event['name'])
                category.save()

            else:
                category = Category.objects.get(name=event['name'])
                new_event.category = category

            new_event.category = category
            new_event.open = True
            new_event.save()


        return Response({'message': 'Events were generated', 'data': request.data})

    return Response({'message': 'Error'}) 