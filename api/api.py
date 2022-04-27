from models.graph import Graph
from api.utils import *
from api.helpers import *
from api.seatgeeks import *


def generate_events():
    print('creating a graph from the api data. (Proof of concept)')
    print('Generating events from  the api')
    events_data = get_n_events_within_radius(
        ticketmaster_api_key='LWNGnCyGcACIMnVaw5CvlPGjWehDAFgj')
    events_data_seatgeek = [create_event_seatgeek(
        evt) for evt in get_events_data_seat_geek()]

    events_ticketmaster = [create_event(evt) for evt in events_data]

    all_events = events_ticketmaster + events_data_seatgeek

    return all_events


def load_graph_from_api():

    events = generate_events()

    print(
        f'Finished creating the event nodes with length {len(events)} with events {events}')
    graph = Graph()
    print('Adding nodes to the graph. Associating nodes that are close.')
    for event1 in events:
        for event2 in events:
            if event1 != event2:
                is_edge, distance = within_range(event1, event2, 250)
                if is_edge:
                    graph.add_edge(event1, event2, distance)

    return graph


def load_events_to_database():
    print('***----****------****-------****------')
    print('Loading data from the api to the database ')

    events = generate_events()
    events = [evt.to_database() for evt in events]
 

    db.insert_events(events)
    print('Finished  populating the database')


def load_events_from_db_to_graph():
    print(f'%%---- %%%------%%%%')
    print('Loading data from the database to the api....')
    load_events_to_database()
    graph=Graph()
    events = []
    for event in db.get_events():

        if event is not None:
            events.append(create_event_from_db(event))
    # print(len(events))
    for event1 in events:
        for event2 in events:
            if event1 != event2:
                # is_edge, distance = within_range(event1, event2, 250)
                # if is_edge:
                graph.add_edge(event1, event2, 20)

    return graph
