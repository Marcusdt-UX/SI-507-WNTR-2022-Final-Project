import configparser
from api.helpers import *
from configparser import ConfigParser
import requests
from api.helpers import calculate_distance
from database.database import Database
from models.models import *


db = Database()


def search_by_venue(self, param):
    """Params: 
    keyword: str 
    radius : area to be covered 
    unit : String enum:["miles", "km"] 
    countryCode : str 



    """
    data = requests.get(URL.venue_url, params=param)
    data = data.json()

    embedded_data = data['_embedded']['venues']
    venues = [create_venue(venue) for venue in embedded_data]
    return venues


def search_by_suggestion(self, url, param):
    """Param is a dict 
    keyword : str 
    countryCode : Filter the suggestion by the countryCode 
    startEndDateTime : Filter when the event should start 

    """
    data = requests.get(URL.suggest_url, param=param)
    data = data.json()


def get_events_within_range(from_date, to_date, ticketmaster_api_key):
    events_url = URL.events_url
    response = requests.get(events_url, params={
        'countryCode': 'US',
        'classificationName': 'Musician',
        'size': 200,
        'startDateTime': from_date.isoformat(),
        'endDateTime': to_date.isoformat(),
        'apikey': ticketmaster_api_key
    })

    json = response.json()
    if '_embedded' in json:
        return response.json()['_embedded']['events']
    else:
        return []


def get_events_within_radius(ticketmaster_api_key='LWNGnCyGcACIMnVaw5CvlPGjWehDAFgj', radius=5):
    events_url = URL.events_url

    response = requests.get(events_url, params={
        'countryCode': 'US',
        'classificationName': 'Musician',
        'size': 200,
        'radius': radius,
        'apikey': ticketmaster_api_key
    })

    json = response.json()
    if '_embedded' in json:
        next_link = URL.root_url + json['_links']['next']['href'] or None
        return response.json()['_embedded']['events'], next_link
    else:
        return []




def get_n_events_within_radius(ticketmaster_api_key='LWNGnCyGcACIMnVaw5CvlPGjWehDAFgj', radius=500):
    events = []
    evts, next_link = get_events_within_radius(
        radius=5, ticketmaster_api_key=ticketmaster_api_key)
    next_link = next_link + f'&apikey={ticketmaster_api_key}'

    events.extend(evts)
    for i in range(1):
        data = requests.get(next_link).json()
        if 'fault' in data or 'error' in data:
            print(data)
        events.extend(data['_embedded']['events'])
        next_link = URL.root_url + \
            data['_links']['next']['href'] + \
            f'&apikey={ticketmaster_api_key}' or None

        if not next_link:
            break
    return events


def get_n_events_within_range(from_date, to_date, ticketmaster_api_key, n=1000):
    total_count = (n//200) - 1

    events = []

    evts, next_link = get_n_events_within_range(
        from_date, to_date, ticketmaster_api_key)
    events.append(evts)
    for _ in range(total_count):
        data = requests.get(next_link).json()
        events.append(data['_embedded']['events'])
        next_link = URL.root_url + data['_link']['next']['href'] or None

        if not next_link:
            break


def within_range(event1, event2, radius):
    distance = calculate_distance(event1.get_location(), event2.get_location())

    if distance <= radius:
        return True, distance

    return None, None


def read_config():
    parser = ConfigParser()
    parser.read('data/config.ini')

    return parser


def read_ticket_master():
    config = read_config()

    return config['ticketmaster']['apikey']


def read_seatgeek():
    config = read_config()
    return config['seatgeek']['client_id'], config['seatgeek']['client_secret']
