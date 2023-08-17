import requests
import json
from sber.data import GIS_TOKEN


def get_route(events):
    url = f'http://routing.api.2gis.com/routing/7.0.0/global?key={GIS_TOKEN}'
    headers = {
        'Content-Type': 'application/json',
    }
    json_routes_data = {
        'points': [],
        'transport': 'pedestrian',
        'params': {
            'pedestrian': {
                'use_instructions': False
            },
        },
        'output': 'summary'
    }

    for event in events:
        if event == events[0] or event == events[-1]:
            json_routes_data['points'].append({
                'lat': event['point']['lat'],
                'lon': event['point']['lon'],
                'type': 'walking'
            })

        else:
            json_routes_data['points'].append({
                'lat': event['point']['lat'],
                'lon': event['point']['lon'],
                'type': 'pref'
            })

    route_response = requests.post(url=url, headers=headers,
                                   json=json_routes_data)

    return route_response.json()


# print(get_route([{"id": "1267165676176619", "name": "Городской дом музыки", "type": "branch", "flags": {"photos": True}, "point": {"lat": 56.850908, "lon": 60.606556}, "reviews": {"items": [{"tag": "2gis_reviews", "is_reviewable": True}, {"tag": "flamp", "rating": 4.3, "review_count": 20, "is_reviewable": True, "recommendation_count": 2}], "rating": 4.3, "org_rating": 4.4, "review_count": 20, "is_reviewable": True, "general_rating": 4.4, "org_review_count": 28, "general_review_count": 28, "recommendation_count": 2, "is_reviewable_on_flamp": True, "org_review_count_with_stars": 32, "general_review_count_with_stars": 32}, "schedule": {"Fri": {"working_hours": [{"to": "20:00", "from": "10:00"}]}, "Mon": {"working_hours": [{"to": "20:00", "from": "10:00"}]}, "Sat": {"working_hours": [{"to": "20:00", "from": "10:00"}]}, "Sun": {"working_hours": [{"to": "20:00", "from": "10:00"}]}, "Thu": {"working_hours": [{"to": "20:00", "from": "10:00"}]}, "Tue": {"working_hours": [{"to": "20:00", "from": "10:00"}]}, "Wed": {"working_hours": [{"to": "20:00", "from": "10:00"}]}}, "address_name": "улица Свердлова, 30"},
#                         {"id": "1267165676192711", "name": "Музей истории Екатеринбурга", "type": "branch", "flags": {"photos": True}, "point": {"lat": 56.840601, "lon": 60.611501}, "reviews": {"items": [{"tag": "2gis_reviews", "is_reviewable": True}, {"tag": "flamp", "rating": 4.3, "review_count": 132, "is_reviewable": True, "recommendation_count": 32}], "rating": 4.3, "org_rating": 4.1, "review_count": 132, "is_reviewable": True, "general_rating": 4.1, "org_review_count": 188, "general_review_count": 188, "recommendation_count": 32, "is_reviewable_on_flamp": True, "org_review_count_with_stars": 210, "general_review_count_with_stars": 210}, "schedule": {"Fri": {"working_hours": [{"to": "18:00", "from": "10:00"}]}, "Sat": {"working_hours": [{"to": "18:00", "from": "11:00"}]}, "Sun": {"working_hours": [{"to": "18:00", "from": "11:00"}]}, "Thu": {"working_hours": [{"to": "19:00", "from": "10:00"}]}, "Wed": {"working_hours": [{"to": "19:00", "from": "10:00"}]}}, "full_name": "Екатеринбург, Музей истории Екатеринбурга", "address_name": "Карла Либкнехта, 26", "purpose_name": "Музей", "building_name": "Музей истории Екатеринбурга"}, 	{"id": "1267166676198079", "name": "Свердловская государственная детская филармония, Главный зал", "type": "branch", "flags": {"photos": True}, "point": {"lat": 56.829426, "lon": 60.600885}, "reviews": {"items": [{"tag": "2gis_reviews", "is_reviewable": True}, {"tag": "flamp", "rating": 4.5, "review_count": 131, "is_reviewable": True, "recommendation_count": 30}], "rating": 4.5, "org_rating": 4.6, "review_count": 131, "is_reviewable": True, "general_rating": 4.6, "org_review_count": 162, "general_review_count": 162, "recommendation_count": 30, "is_reviewable_on_flamp": True, "org_review_count_with_stars": 187, "general_review_count_with_stars": 187}, "schedule": {"Fri": {"working_hours": [{"to": "19:30", "from": "09:30"}]}, "Mon": {"working_hours": [{"to": "19:30", "from": "09:30"}]}, "Sat": {"working_hours": [{"to": "18:00", "from": "09:30"}]}, "Sun": {"working_hours": [{"to": "18:00", "from": "09:30"}]}, "Thu": {"working_hours": [{"to": "19:30", "from": "09:30"}]}, "Tue": {"working_hours": [{"to": "19:30", "from": "09:30"}]}, "Wed": {"working_hours": [{"to": "19:30", "from": "09:30"}]}}, "full_name": "Екатеринбург, Свердловская государственная детская филармония", "address_name": "8 Марта, 36", "purpose_name": "Культурное учреждение", "building_name": "Свердловская государственная детская филармония"}]))