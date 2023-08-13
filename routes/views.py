import json
import random
import requests
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from routes.models import Route
from routes.serializers import RouteSerializer


class RouteAPIListCreateView(generics.ListCreateAPIView):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = [IsAuthenticated]

    def get_city(self, city):
        token_key = '5ae2e3f221c38a28845f05b61e9871acfa940c8d8073e83925042c84'
        city_url = f'http://api.opentripmap.com/0.1/ru/places/geoname'
        params = {
            'name': city,
            'apikey': token_key
        }
        city_response = requests.get(city_url, params=params)

        return {'lat': city_response.json()['lat'],
                'lon': city_response.json()['lon']}


    def get_places(self, city):
        token_key = '5ae2e3f221c38a28845f05b61e9871acfa940c8d8073e83925042c84'
        places_url = f'http://api.opentripmap.com/0.1/ru/places/radius'
        params = {
            'radius': 50000,
            'lat': city['lat'],
            'lon': city['lon'],
            'kinds': 'history_museums,art_galleries,opera_houses',
            'limit': 15,
            'apikey': token_key
        }
        places_response = requests.get(places_url, params=params).json()['features']
        places_data = []

        for place in places_response:
            place_data = {}
            place_data['name'] = place['properties']['name']
            place_data['lat'] = place['geometry']['coordinates'][1]
            place_data['lon'] = place['geometry']['coordinates'][0]
            place_data['rate'] = place['properties']['rate']
            place_data['kinds'] = place['properties']['kinds']

            places_data.append(place_data)

        return places_data
    
    def perform_create(self, serializer):
        route_result = self.get_places(self.get_city('Екатеринбург'))
        
        serializer.save(waypoints=route_result)
    

class RouteAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = [IsAuthenticated]


class RouteAPITicketGetView(generics.UpdateAPIView):
    serializer_class = RouteSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        obj = Route.objects.get(pk=self.kwargs['pk'])
        customer = self.request.user

        obj.tickets.add(customer.pk)
        obj.save()

        serializer = RouteSerializer(obj, required=False)

        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)
    

class RouteAPIMyTicketsView(generics.ListAPIView):
    serializer_class = RouteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.routes_user.all()