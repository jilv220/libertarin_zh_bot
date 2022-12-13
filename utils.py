import json

def get_handles():
    f = open('config.json')
    data = json.load(f)
    f.close()
    return data['handles']