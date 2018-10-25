import os 
import json
import datetime


def dump_on_disk(data, path, fmt='json'):
    """
    Dump given data into a file on the disk
    
    Args:
        data (str): data to be dumped
        path (str): path where the output file should be located
        fmt (str, optional): Defaults to 'json'. Format of output file.
    """

    timestamp = datetime.datetime.now().isoformat()

    if fmt not in ['json', 'txt']:
        raise AttributeError('Please enter a valid file format')

    with open(path, 'w') as outfile:
        json.dump(data, outfile)
