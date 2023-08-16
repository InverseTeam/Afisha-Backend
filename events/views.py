import json
import requests
from rest_framework.decorators import api_view
from faker import Faker
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from events.models import *
from events.serializers import *
from events.gis import get_place_by_name_2gis
from users.permissions import IsManagerOrAdminOrReadOnly
from django.core.files.base import ContentFile
from sber.data import GIS_TOKEN


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
        return Event.objects.filter(published=True)


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
        published = self.request.GET.get('published', None)

        if desired_date: events = events.filter(date=desired_date)
        if category: events = events.filter(category=category)
        if age_limit: events = events.filter(age_limit__lte=age_limit)
        if pushkin_payment: events = events.filter(pushkin_payment=pushkin_payment)
        if published: events = events.filter(published=published)
        
        if tags: 
            tags = tags.split(',')
            events = events.filter(tags__in=tags)

        return events
    

class EventAPIFavoritesListView(generics.ListAPIView):
    serializer_class = EventReadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.favorites.all()
    

class EventAPIFavoritesAddView(generics.UpdateAPIView):
    serializer_class = EventReadSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        obj = Event.objects.get(pk=self.kwargs['pk'])
        user = self.request.user

        user.favorites.add(obj.pk)
        user.save()

        serializer = EventReadSerializer(obj, required=False)

        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)
    

class EventAPIFavoritesRemoveView(generics.UpdateAPIView):
    serializer_class = EventReadSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        obj = Event.objects.get(pk=self.kwargs['pk'])
        user = self.request.user

        user.favorites.remove(obj.pk)
        user.save()

        serializer = EventReadSerializer(obj, required=False)

        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)
    

class EventAPIAddPushkinWantView(generics.UpdateAPIView):
    serializer_class = EventReadSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        obj = Event.objects.get(pk=self.kwargs['pk'])
        obj.want_pushkin += 1
        obj.save()

        serializer = EventReadSerializer(obj, required=False)

        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)
    

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

    
@api_view(['POST'])
def generate_events(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name', None)
        category = data.get('category', None)
        total_tickets = data.get('total_tickets', None)
        price = data.get('price', None)
        age_limit = data.get('age_limit', None)
        tags = data.get('tags', None)
        description = data.get('description', None)
        artist = data.get('artist', None)
        platform = data.get('platform', None)
        address = data.get('address', None)
        date = data.get('date', None)
        event_time = data.get('time', None)
        cover = data.get('cover', None)
        pushkin_pay = data.get('pushkin_payment', None)

        if not Event.objects.filter(name=name).exists():
            event = Event(name=name, total_tickets=total_tickets, price=price,
                            age_limit=age_limit, description=description, artist=artist,
                            date=date, time=event_time, pushkin_payment=pushkin_pay)
            
            if cover:
                image = requests.get(cover)
                image_data = ContentFile(image.content)
                image_name = str(uuid.uuid4())
                event.cover.save(f'{image_name}.png', image_data, save=True)

            if not Category.objects.filter(name=category).exists():
                Category.objects.create(name=category)

            event.category = Category.objects.get(name=category)

            if tags:
                for tag in tags:
                    if not Tag.objects.filter(name=tag).exists():
                        Tag.objects.create(name=tag)

                    tag_obj = Tag.objects.get(name=tag)
                    event.tags.add(tag_obj)

                    if tag_obj not in event.category.tags.all():
                        category_obj = event.category
                        category_obj.tags.add(tag_obj.pk)
                        category_obj.save() 

            if not Platform.objects.filter(name=platform).exists():
                platform_data = get_place_by_name_2gis(f'{platform}, {address}')
                Platform.objects.create(name=platform, address=address, location_data=platform_data)

            event.platform = Platform.objects.get(name=platform)
            event.save()

            return Response({'message': 'Events were generated', 'data': request.data})

    return Response({'message': 'Error'}) 