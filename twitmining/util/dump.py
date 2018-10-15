import os 
import json
import datetime

def dump_on_disk(data, format='json'):
    timestamp = datetime.datetime.now().isoformat()
    if format not in ['json', 'txt']:
        raise AttributeError('Please enter a valid file format')
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'history/twitmining_request_' + timestamp + '.' + format)
    with open(path, 'w') as outfile:
        json.dump(data, outfile)
