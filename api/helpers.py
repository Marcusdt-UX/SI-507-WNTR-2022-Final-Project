import math
import random
from models.models import Event
from data.data import data
from datetime import datetime
import requests
from collections import defaultdict



def create_event(event):
    default_image_url = 'https://media.istockphoto.com/photos/cheering-crowd-with-hands-in-air-at-music-festival-picture-id1247853982?k=20&m=1247853982&s=612x612&w=0&h=QyAzDkXf7kr7ZljPCsdIrpREnqBRpb0ybotTQ7037cA='
    process_image = event['images']

    image_url = ''
    if process_image:
        image_url = process_image[0]['url']
    else:
        image_url = default_image_url
    evt = Event(id_=event['id'], name=event['name'], type_=event['type'], locale=event['locale'],
                url=event['url'], images= image_url, sales=event['sales'], venues=event['_embedded']['venues'][0], dates=event['dates'].get(
                    'start').get('localDate'),
                                    classifications='',description=event['name']

                
                )

    return evt


def create_event_seatgeek(event):
    default_image_url = 'https://media.istockphoto.com/photos/cheering-crowd-with-hands-in-air-at-music-festival-picture-id1247853982?k=20&m=1247853982&s=612x612&w=0&h=QyAzDkXf7kr7ZljPCsdIrpREnqBRpb0ybotTQ7037cA='

    evt = Event(id_=event['id'], name=event['title'], type_=event['type'], locale='en', url=event['url'],images=default_image_url, longitude=event['venue']['location']['lon'],
                latitude=event['venue']['location']['lat'], dates=event['datetime_local'],
                location=event['venue'], price_range=event['stats']['average_price'],description=event['title']
                )

    return evt


def create_event_from_db(row):
    # id,name,type,url,localDate,classificationsSegmentID

    evt = Event(id_=row[0], name=row[1], type_=row[2],
                url=row[3], dates=row[4], classifications=row[5],images=row[6])

    return evt


def search_events(self, url):
    data = requests.get(url).json()
    events = data['_embedded']["events"]

    events = [create_event(event) for event in events]
    return events



def calculate_distance(origin, destination):

    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) * math.sin(dlon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radius * c

    return d




def filter_by_country(country, data=data):
    print(f'Country chosen is {country} with {data.get_country(country)}')
    ticketmaster_api_key='LWNGnCyGcACIMnVaw5CvlPGjWehDAFgj'
    url = 'https://app.ticketmaster.com/discovery/v2/events.json'
    params = {
       'countryCode':data.get_country(country),
       'size' : 200,
       'apikey':ticketmaster_api_key

    }

    data = requests.get(url,params=params).json()
    if '_embedded' in data:
        data = data['_embedded']['events']
        events = [create_event(event) for event in data]
        random.shuffle(events)
        return events 

    else:
        return []
   


def filter_by_keyword(country='united states',keyword='house',data=data):
    print('In the filter by keyword')
    ticketmaster_api_key='LWNGnCyGcACIMnVaw5CvlPGjWehDAFgj'
    url = 'https://app.ticketmaster.com/discovery/v2/events.json'
    params = {
        'keyword':keyword,
        'countryCode':'US',
        'size':200,
        'apikey':ticketmaster_api_key
    }

    data = requests.get(url,params=params).json()
    if '_embedded' in data:
        data = data['_embedded']['events']
        events = [create_event(event) for event in data]
        random.shuffle(events)
        print(f'Total events in keyword is {len(events)}')
        return events 

    else:
        return []


def filter_by_state(country='united states',state='illinois',radius='10',data=data):
    ticketmaster_api_key='LWNGnCyGcACIMnVaw5CvlPGjWehDAFgj'
    url = 'https://app.ticketmaster.com/discovery/v2/events.json'

    params = {
        'countryCode':data.get_country(country),
        'size': 100,
        'radius':radius,
        'stateCode': data.get_state(state.lower()),
        'apikey':ticketmaster_api_key
    }
    
    data = requests.get(url,params=params).json()
    if '_embedded' in data:
        data = data['_embedded']['events']
        events = [create_event(event) for event in data]
        random.shuffle(events)
        return events 
    else:
        return []
   

def filter_events_by_date(from_date:datetime, to_date:datetime):
    ticketmaster_api_key='LWNGnCyGcACIMnVaw5CvlPGjWehDAFgj'

    url = 'https://app.ticketmaster.com/discovery/v2/events.json'

    data = requests.get(url, params={
        'countryCode': 'US',
        'size': 200,
        'startDateTime': from_date.isoformat(),
        'endDateTime': to_date.isoformat(),
        'apikey': ticketmaster_api_key
    }).json()

    if '_embedded' in data:
        data = data['_embedded']['events']
        events = [create_event(event) for event in data]

        random.shuffle(events)
        return events 

    else:
        return []

def filter_events_by_current_location(lat,long,radius=10):

    ticketmaster_api_key='LWNGnCyGcACIMnVaw5CvlPGjWehDAFgj'
    url = 'https://app.ticketmaster.com/discovery/v2/events.json'
    loc = lat+','+long

    params = {
        'size': 100,
        'radius':radius,
        'latlong':loc,
        'apikey':ticketmaster_api_key
    }
    
    data = requests.get(url,params=params).json()

    if '_embedded' in data:
        events =  data['_embedded']['events']
        events_made = [create_event(event) for event in events]
        random.shuffle(events_made)
        return events_made
    else:
        return  []

    


def delegator(**kwargs):
   
    if 'state' in kwargs:
        if 'radius' in kwargs:  
            evt =  filter_by_state(state=kwargs.get('state'),radius=kwargs.get('radius'))
            return evt

        
        evt =  filter_by_state(state=kwargs.get('state'))
        return evt
    elif 'keyword' in kwargs:
        
        return filter_by_keyword(keyword=kwargs.get('keyword'))

     
    elif 'from_date' in kwargs:

        return filter_events_by_date(lat=kwargs.get('from_date'),long=kwargs.get('to_date'))

    elif 'lat' in kwargs:
        if 'radius' in kwargs:
            return filter_events_by_current_location(lat=kwargs.get('lat'),long=kwargs.get('long'),radius=kwargs.get('radius'))
        return filter_events_by_current_location(lat=kwargs.get('lat'),long=kwargs.get('lon'))

    elif 'country' in kwargs:
        output =  filter_by_country(kwargs.get('country'))
        return output


def filter_dups(events):
    sieve = {}
    result = []

    for event in events:
        if event.name not in sieve:
            sieve[event.name] = 0 
            result.append(event)

    return result





    

    


