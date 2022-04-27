from api.utils import *


class Event:
    def __init__(
        self, id_, name=None, type_=None,
        locale=None, url=None, sales=None, dates=None, price_range=None,
        attractions=None, images=None, venues=None, info=None, classifications=None, longitude=None,
        latitude=None, location=None,description = None

    ) -> None:
        self.id = id_
        self.name = name
        self.type = type_
        self.locale = locale
        self.url = url
        self.sales = sales
        self.dates = dates
        self.attractions = attractions
        self.images = images
        self.venue = venues
        self.info = info
        self.classificationsSegmentID = classifications
        self.longitude = longitude
        self.latitude = latitude
        self.location = location
        self.price_range = price_range
        self.description = description 

        # if self.venue:
        #     self.longitude = self.venue['location']['longitude']
        #     self.latitude = self.venue['location']['latitude']

    def __str__(self) -> str:
        print(f'{self.id}, {self.name} {self.type} {self.url}')

    def get_location(self):
        return float(self.latitude), float(self.longitude)

    def to_database(self):
        return (self.id, self.name, self.type, self.url, self.dates, self.classificationsSegmentID, str(self.price_range), str(self.longitude), str(self.latitude),str(self.images))




def generate_address(self):
    return [self.city, self.state['name'], self.state['code'], self.country, self.location['latitude'], self.location['longituide'], self.id]


class Image:
    def __init__(self, ratio, url, height, width, fallback) -> None:
        self.ration = ratio
        self.url = url
        self.height = height
        self.width = width,
        self.fallback = fallback


class EventHandler:
    """Loads data  to the database

    """

    def __init__(self, events) -> None:
        self.events = events


class URL:
    root_url = 'https://app.ticketmaster.com'
    base_url = 'https://app.ticketmaster.com/discovery/v2/events.json'
    venue_url = "https://app.ticketmaster.com/discovery/v2/venues.json?keyword=UCV&apikey=LWNGnCyGcACIMnVaw5CvlPGjWehDAFgj"
    events_url = 'https://app.ticketmaster.com/discovery/v2/events.json'
    suggest_url = "https://app.ticketmaster.com/discovery/v2/suggest"
