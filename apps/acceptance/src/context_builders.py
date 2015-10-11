import json
import requests
from yatu.utils import make_uri


def make_short_it_request(data):
    data_json = json.dumps(data)
    headers = {'Content-type': 'application/json'}
    result = requests.post(make_uri("short_it/"),
                           data=data_json,
                           headers=headers)

    return result.json(), result.status_code

