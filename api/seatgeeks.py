import requests
from api.helpers import create_event_seatgeek

from api.utils import read_seatgeek

clientID, clientSecret = read_seatgeek()

seatgeeks_url = f'https://api.seatgeek.com/2/events?client_id={clientID}&client_secret={clientSecret}'


def get_events_data_seat_geek(params={}):
    # Extract the data
    data = requests.get(seatgeeks_url, params=params).json()

    events = [event for event in data['events']]

    return events

