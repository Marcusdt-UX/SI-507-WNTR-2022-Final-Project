import json
def read_json(filename):

    with open(filename) as f:
        data = json.load(f)

    return data 

data = read_json('output_events.json')
