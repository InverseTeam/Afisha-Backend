import requests
from faker import Faker
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from events.models import *
from events.serializers import *
from events.parser import get_events
from users.permissions import IsManagerOrAdminOrReadOnly
from users.models import CustomUser
from rest_framework.decorators import api_view
from django.core.files.base import ContentFile


class EventAPIListCreate(generics.ListCreateAPIView):
    serializer_class = EventReadSerializer
    permission_classes = [IsManagerOrAdminOrReadOnly]

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
    

class EventAPIFilterListView(generics.ListAPIView):
    serializer_class = EventReadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        events = Event.objects
        desired_date = self.request.GET.get('date', None)
        category = self.request.GET.get('category', None)
        tags = self.request.GET.get('tags', None)
        age_limit = self.request.GET.get('age_limit', None)
        pushkin_payment = self.request.GET.get('pushkin_payment', None)

        if desired_date: events = events.filter(performances__date=desired_date)
        if category: events = events.filter(category=category)
        if age_limit: events = events.filter(age_limit__lte=age_limit)
        if pushkin_payment: pushkin_payment = events.filter(pushkin_payment=pushkin_payment)
        
        if tags: 
            tags = tags.split(',')
            events = events.filter(tags__in=tags)

        return events


class EventAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventReadSerializer
    permission_classes = [IsManagerOrAdminOrReadOnly]

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
    

class EventImageAPICreateView(generics.CreateAPIView):
    serializer_class = EventImageSerializer
    permission_classes = [IsManagerOrAdminOrReadOnly]
    

class PlatformAPIListCreateView(generics.ListCreateAPIView):
    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer
    permission_classes = [IsManagerOrAdminOrReadOnly]


class PlatformAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer
    permission_classes = [IsManagerOrAdminOrReadOnly]


class CategoryAPIListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsManagerOrAdminOrReadOnly]


class TagAPIListCreateView(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsManagerOrAdminOrReadOnly]


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


class ArtistAPIListCreateView(generics.ListCreateAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = [IsAuthenticated]


class ArtistsAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = [IsAuthenticated]


class TicketAPICreateView(generics.CreateAPIView):
    serializer_class = TicketWriteSerializer
    permission_classes = [IsAuthenticated]


    def post(self, request, *args, **kwargs):
        serializer = TicketWriteSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            ticket = Ticket.objects.get(pk=serializer.data['id'])
            
            performance = Performance.objects.get(pk=self.kwargs['pk'])
            performance.tickets.add(ticket.pk)
            performance.save()

            ticket_type = ticket.ticket_type
            ticket_type.tickets_sold += 1
            ticket_type.save()

            if ticket_type.tickets_sold == ticket_type.tickets_number:
                ticket_type.open = False
                ticket_type.save()

            ticket_types_open = []

            for type_ticket in performance.ticket_types.all():
                ticket_types_open.append(type_ticket.open)

            if True in ticket_types_open:
                performance.open = False
                performance.save()

            events = performance.events_performance.all()
            performances_open = []

            for event in events:
                for event_performance in event.performances.all():
                    performances_open.append(event_performance.open)

                if True in performances_open:
                    event.open = False

                event.tickets_sold += 1
                event.save()

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