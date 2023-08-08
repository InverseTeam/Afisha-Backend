from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from events.models import *
from events.serializers import *
from users.models import CustomUser
from users.permissions import IsManager


class EventAPIListCreate(generics.ListCreateAPIView):
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
    
    def get_queryset(self):
        return Event.objects.filter(artists__manager__pk=self.request.user.pk)


class EventAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
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
    

class EventAPITicketBuyView(generics.UpdateAPIView):
    serializer_class = EventWriteSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        obj = Event.objects.get(pk=self.kwargs['pk'])
        customer = self.request.user

        customer.money -= obj.price

        obj.tickets.add(customer.pk)
        obj.save()
        customer.save()

        serializer = EventWriteSerializer(obj, required=False)

        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)
    

class EventAPIMyTicketsView(generics.ListAPIView):
    serializer_class = EventReadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.events_user.all()
    

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


class TagAPIListView(generics.ListAPIView):
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Category.objects.get(pk=self.kwargs['pk']).tags.all()


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
    

class EntryConditionAPIListView(generics.ListAPIView):
    queryset = EntryCondition.objects.all()
    serializer_class = EntryConditionSerializer
    permission_classes = [IsAuthenticated]


class PerformanceAPICreate(generics.CreateAPIView):
    serializer_class = PerformanceSerializer
    permission_classes = [IsManager]

    def post(self, request, *args, **kwargs):
        serializer = PerformanceSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            performance = Performance.objects.get(pk=serializer.data['id'])
            event = Event.objects.get(pk=self.kwargs['pk'])
            event.performances.add(performance.pk)
            performance.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        

class TicketTypeAPICreate(generics.CreateAPIView):
    serializer_class = TicketTypeSerializer
    permission_classes = [IsManager]

    def post(self, request, *args, **kwargs):
        serializer = TicketTypeSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            ticket_type = TicketType.objects.get(pk=serializer.data['id'])
            performance = Performance.objects.get(pk=self.kwargs['pk'])
            performance.ticket_types.add(ticket_type.pk)
            performance.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)