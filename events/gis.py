import requests
import json
from sber.data import GIS_TOKEN


def get_place_by_name_2gis(name):
    places_url = f'https://catalog.api.2gis.com/3.0/items'
    places_params = {
        'q': name,
        'city_id': '1267260165455895',
        'page_size': 1,
        'fields': 'items.id,items.name,items.adress,items.point,'
                  'items.schedule,items.reviews,items.flags, photos.l',
        'key': GIS_TOKEN
    }
    places_response = requests.get(places_url, params=places_params,
                                   headers= {'Content-Type': 'text/html'})

    return places_response.json()['result']['items'][0]


