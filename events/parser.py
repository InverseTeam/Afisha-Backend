import requests
import re
from bs4 import BeautifulSoup
import json


def get_sport_event(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    try:
        event = {
            'name': re.sub("^\s+|\n|\r|\s+$", '', soup.find('h1', attrs={'class': 'hidden-xs'}).text),
            'start_date': re.sub("^\s+|\n|\r|\s+$", '', soup.find('div', attrs={'class': 'start-date'}).text),
            'description': re.sub("^\s+|\n|\r|\s+$", '', '\n\n'.join([element.text for element in soup.find('div', attrs={'class': 'description'}).find_all('p')])),
            'platform': re.sub("^\s+|\n|\r|\s+$", '', soup.find('div', attrs={'class': 'breadcrumb'}).find_all('span')[2].find('a').text),
            'location': re.sub("^\s+|\n|\r|\s+$", '', ', '.join([element.text for element in soup.find('div', attrs={'class': 'location'}).find_all('span')])),
            'age_category': re.sub("^\s+|\n|\r|\s+$", '', soup.find('div', attrs={'class': 'event__age-restriction'}).text),
            'cover': 'https://afisha-ekb.ru/' + soup.find('a', class_=['image-link', 'event-image']).attrs['href']
        }

    except:
        return None

    return event


def get_events():
    response = requests.get('https://afisha-ekb.ru/list/sport/?ysclid=ll84dgik8p437560618&page=1')
    soup = BeautifulSoup(response.text, 'lxml')
    pages_num = int(soup.find('ul', attrs={'class': 'pagination'}).find_all('a')[-3].text)
    pages = []

    for i in range(1, pages_num + 1):
        page_url = f'https://afisha-ekb.ru/list/sport/?ysclid=ll84dgik8p437560618&page={i}'
        page_response = requests.get(page_url)
        page_soup = BeautifulSoup(page_response.text, 'lxml')
        events = page_soup.find_all('div', class_=['event-info'])

        for event in events:
            event_data = get_sport_event(f'https://afisha-ekb.ru{event.find("a").attrs["href"]}')
            if event_data:
                pages.append(event_data)

    return pages