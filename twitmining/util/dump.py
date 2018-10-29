import os 
import json
import datetime


def dump_on_disk(data, fmt='json'):
    """
    Dump given data into a file on the disk
    
    Args:
        data (dict): data to be dumped
        fmt (str, optional): Defaults to 'json'. Format of output file.
    """

    timestamp = datetime.datetime.now().isoformat()

    if fmt not in ['json', 'txt']:
        raise AttributeError('Please enter a valid file format')

    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'history/twitmining_request_' + timestamp + '.' + fmt)

    with open(path, 'w') as outfile:
        json.dump(data, outfile)
