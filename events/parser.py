import requests
import re
from bs4 import BeautifulSoup
import json
import random
import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By


driver = webdriver.Firefox()


def parse_date(str_date, year):
    date = str_date.lower().split(' ')
    months_starts = ['янв', 'фев', 'мар', 'апр', 'мая', 'июн',
                     'июл', 'авг', 'сен', 'окт', 'ноя', 'дек']

    for month in months_starts:
        if date[1].startswith(month):
            return datetime.date(year, months_starts.index(month) + 1, int(date[0]))


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


def get_movie(url):
    driver.get(url)
    scroll_js = "arguments[0].scrollIntoView();"
    try:
        recent_views = driver.find_element(By.CLASS_NAME, 'viewed-events')
    except:
        pass
    else:
        driver.execute_script(scroll_js, recent_views)

    time.sleep(1)

    category_tags = [tag.text for tag in
                     driver.find_element(By.CLASS_NAME, 'tags').find_elements(By.CLASS_NAME, 'tags__item')]
    event_json = {
        'name': driver.find_element(By.CLASS_NAME, 'event-concert-description__title-info').text,
        'category': category_tags[0],
        'total_tickets': random.randint(200, 1000),
        'price': random.choice([150, 250, 300, 500, 1000, 1200])
    }

    try: age_limit = int(re.findall('\d+', driver.find_element(By.CLASS_NAME, 'event-concert-heading__content-rating').text)[0])
    except: pass
    else: event_json['age_limit'] = age_limit

    try: tags = category_tags[1:]
    except: pass
    else: event_json['tags'] = tags

    try: description = driver.find_element(By.CLASS_NAME, 'concert-description__text').text
    except: pass
    else: event_json['description'] = description

    try: platform = driver.find_element(By.CLASS_NAME, 'Name-sc-1trqzwk-4').text
    except: pass
    else: event_json['platform'] = platform

    try: address = driver.find_element(By.CLASS_NAME, 'afisha-common-venue-address').text
    except: pass
    else: event_json['address'] = address

    try: cover = recent_views.find_element(By.XPATH, ".//img").get_attribute("src")
    except: return None
    else: event_json['cover'] = cover

    try: pushkin_pay = driver.find_element(By.CLASS_NAME, 'pushkin-card-badge-react')
    except: event_json['pushkin_payment'] = False
    else: event_json['pushkin_payment'] = True

    return event_json


def get_event(url):
    driver.get(url)
    scroll_js = "arguments[0].scrollIntoView();"
    try:
        recent_views = driver.find_element(By.CLASS_NAME, 'viewed-events')
    except:
        pass
    else:
        driver.execute_script(scroll_js, recent_views)

    time.sleep(1)

    category_tags = [tag.text for tag in
                     driver.find_element(By.CLASS_NAME, 'tags').find_elements(By.CLASS_NAME, 'tags__item')]
    event_json = {
        'name': driver.find_element(By.CLASS_NAME, 'event-concert-description__title-info').text,
        'category': category_tags[0],
        'total_tickets': random.randint(200, 1000),
        'price': random.choice([150, 250, 300, 500, 1000, 1200])
    }

    try: age_limit = int(re.findall('\d+', driver.find_element(By.CLASS_NAME, 'event-concert-heading__content-rating').text)[0])
    except: pass
    else: event_json['age_limit'] = age_limit

    try: tags = category_tags[1:]
    except: pass
    else: event_json['tags'] = tags

    try: description = driver.find_element(By.CLASS_NAME, 'concert-description__text').text
    except: pass
    else: event_json['description'] = description

    try: artist = driver.find_element(By.CLASS_NAME, 'ChipInner-wr23a4-1').text.replace('\n', ' ')
    except: pass
    else: event_json['artist'] = artist

    try: platform = driver.find_element(By.CLASS_NAME, 'place__title').text
    except: pass
    else: event_json['platform'] = platform

    try: address = driver.find_element(By.CLASS_NAME, 'place__address').text
    except: pass
    else: event_json['address'] = address

    try: date = str(parse_date(driver.find_element(By.CLASS_NAME, 'session-date__day').text, 2023))
    except: pass
    else: event_json['date'] = date

    try: event_time = str(datetime.datetime.strptime(driver.find_element(By.CLASS_NAME, 'session-date__time').text, '%H:%M').time())
    except: pass
    else: event_json['time'] = event_time

    try: cover = recent_views.find_element(By.XPATH, ".//img").get_attribute("src")
    except: return None
    else: event_json['cover'] = cover

    try: pushkin_pay = driver.find_element(By.CLASS_NAME, 'pushkin-card-badge-react')
    except: event_json['pushkin_payment'] = False
    else: event_json['pushkin_payment'] = True

    return event_json


def get_urls_events(url):
    driver.get(url)

    while True:
        try:
            more_button = driver.find_element(By.CLASS_NAME, 'button-more')
            more_button.click()
        except:
            break

    events_list = driver.find_element(By.CLASS_NAME, 'events-list__list')
    events_urls = []

    for event in events_list.find_elements(By.CLASS_NAME, 'EventLink-sc-1x07jll-2'):
        events_urls.append(event.get_attribute('href'))

    return events_urls



def generate_data_api(event_urls):
    for url in event_urls:
        event_data = get_event(url)

        if event_data:
            create_event = requests.post('https://inverse-tracker.store/api/events/generate/', json=event_data)

            try:
                print(json.dumps(create_event.json(), indent=4, ensure_ascii=False))
            except:
                continue


def generate_movies_data_api(event_urls):
    for url in event_urls:
        event_data = get_movie(url)

        if event_data:
            create_event = requests.post('https://inverse-tracker.store/api/events/generate/', json=event_data)

            try:
                print(json.dumps(create_event.json(), indent=4, ensure_ascii=False))
            except:
                continue
