import json
import random
import requests
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from routes.models import Route, RouteType
from routes.serializers import RouteTypeSerializer, RouteReadSerializer, RouteWriteSerializer


class RouteAPIListCreateView(generics.ListCreateAPIView):
    queryset = Route.objects.all()
    serializer_class = RouteWriteSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Route.objects.all()
        serializer = RouteReadSerializer(queryset, many=True)
        
        return Response(serializer.data)

    def get_route(self, category, city_id, transport, limit):
        places_url = 'https://catalog.api.2gis.com/3.0/items'
        token_key = 'dcdb5f82-9ab6-4116-ac75-367df24d5560'
        routes_url = f'http://routing.api.2gis.com/routing/7.0.0/global?key={token_key}'
        headers = {
            'Content-Type': 'application/json',
        }
        params = {
            'q': category,
            'city_id': city_id,
            'page_size': limit,
            'fields': 'items.id,items.name,items.adress,items.point,'
                        'items.schedule,items.reviews,items.flags, photos.l',
            'key': token_key
        }
        places_response = requests.get(places_url, params=params)
        places_data = places_response.json()['result']['items']
        json_routes_data = {
            'points': [],
            'transport': transport,
            'output': 'summary'
        }

        for i in range(0, len(places_data) - 1):
            json_routes_data['points'].append([
                {'lat': places_data[i]['point']['lat'], 'lon': places_data[i]['point']['lon']},
                {'lat': places_data[i + 1]['point']['lat'], 'lon': places_data[i + 1]['point']['lon']}
            ])

        routes_response = requests.post(routes_url, headers=headers,
                                        json=json_routes_data)
        routes_data = routes_response.json()
        result_route = []

        for i in range(0, len(places_data) - 1):
            result_route.append({
                'distance': routes_data[i]['distance'],
                'duration': routes_data[i]['duration'] // 60,
                'places': [places_data[i], places_data[i + 1]],
                'points': {'lat1': routes_data[i]['lat1'], 'lat2': routes_data[i]['lat2'],
                            'lon1': routes_data[i]['lon1'], 'lon2': routes_data[i]['lon2']}
            })

        return result_route
    
    def perform_create(self, serializer):
        route_type = RouteType.objects.get(pk=serializer.validated_data['route_type'].pk)
        route_result = self.get_route(category=route_type.query_text, city_id='1267260165455895', transport='pedestrian',
                limit=random.randint(3, 4))
        
        serializer.save(waypoints=route_result)



class RouteAPIFilterListView(generics.ListAPIView):
    serializer_class = RouteReadSerializer
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
    serializer_class = RouteReadSerializer
    permission_classes = [IsAuthenticated]
    

class RouteAPIRouteTypeListView(generics.ListAPIView):
    serializer_class = RouteReadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Route.objects.filter(route_type=self.kwargs['pk'])
    

class RouteTypeAPIListView(generics.ListAPIView):
    queryset = RouteType.objects.all()
    serializer_class = RouteTypeSerializer
    permission_classes = [IsAuthenticated]


class RouteAPITicketBuyView(generics.UpdateAPIView):
    serializer_class = RouteReadSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        obj = Route.objects.get(pk=self.kwargs['pk'])
        customer = self.request.user

        customer.money -= obj.price

        obj.tickets.add(customer.pk)
        obj.save()
        customer.save()

        serializer = RouteReadSerializer(obj, required=False)

        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)
    

class RouteAPIMyTicketsView(generics.ListAPIView):
    serializer_class = RouteReadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.routes_user.all()