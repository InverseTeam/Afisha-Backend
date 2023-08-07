from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from routes.models import Route, RouteType
from routes.serializers import RouteSerializer, RouteTypeSerializer


class RouteAPIListCreateView(generics.ListCreateAPIView):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = [IsAuthenticated]


class RouteAPIFilterListView(generics.ListAPIView):
    serializer_class = RouteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        active = self.request.GET.get('active', None)
        category = self.request.GET.get('category', None)
        price_limit = self.request.GET.get('price_limit', None)
        start_date = self.request.GET.get('start_date', None)
        end_date = self.request.GET.get('end_date', None)

        if active and category and price_limit and start_date and end_date:
            return Route.objects.filter(active=active, route_type=category, price__lt=price_limit, start_date__gte=start_date, end_date__lte=end_date)

        return Response("Something went wrong!", status=status.HTTP_400_BAD_REQUEST)
    

class RouteAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = [IsAuthenticated]
    

class RouteAPIRouteTypeListView(generics.ListAPIView):
    serializer_class = RouteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Route.objects.filter(route_type=self.kwargs['pk'])
    

class RouteTypeAPIListView(generics.ListAPIView):
    queryset = RouteType.objects.all()
    serializer_class = RouteTypeSerializer
    permission_classes = [IsAuthenticated]


class RouteAPITicketBuyView(generics.UpdateAPIView):
    serializer_class = RouteSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        obj = Route.objects.get(pk=self.kwargs['pk'])
        customer = self.request.user

        customer.money -= obj.price

        obj.tickets.add(customer.pk)
        obj.save()
        customer.save()

        serializer = RouteSerializer(obj, required=False)

        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)
    

class RouteAPIMyTicketsView(generics.ListAPIView):
    serializer_class = RouteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.routes_user.all()