from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from events.models import *
from events.serializers import *
from users.models import CustomUser
from users.permissions import IsManager


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
        tags = self.request.GET.get('tags', None)
        price_limit = self.request.GET.get('price_limit', None)
        age_limit = self.request.GET.get('age_limit', None)

        if desired_date: events = events.filter(performances__date=desired_date)
        if category: events = events.filter(category=category)
        if price_limit: events = events.filter(price__lte=price_limit)
        if age_limit: events = events.filter(age_limit__lte=age_limit)
        
        if tags: 
            tags = tags.split(',')
            events = events.filter(tags__in=tags)

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
            performance.save()

            event = Event.objects.get(pk=self.kwargs['pk'])
            event.performances.add(performance.pk)

            if not event.start_date:
                event.start_date = performance.date

            elif not event.end_date:
                event.end_date = performance.date

            elif performance.date < event.start_date:
                event.start_date = performance.date

            elif performance.date > event.end_date:
                event.end_date = performance.date

            event.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        

class PerformancesAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Performance.objects.all()
    serializer_class = PerformanceSerializer
    permission_classes = [IsManager]
        

class TicketTypeAPICreateView(generics.CreateAPIView):
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

            for event in performance.events_performance.all():
                event.tickets_number += ticket_type.tickets_number
                event.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)


class TicketAPICreateView(generics.CreateAPIView):
    serializer_class = TicketWriteSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = TicketWriteSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            ticket = Ticket.objects.get(pk=serializer.data['id'])

            user_buyer = ticket.buyer
            user_buyer.money -= ticket.ticket_type.price
            user_buyer.save()
            
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
        return Ticket.objects.filter(buyer=self.request.user.pk)