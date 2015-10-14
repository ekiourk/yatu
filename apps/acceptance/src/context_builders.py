import json
import requests
from yatu.utils import make_uri


def make_short_it_request(data):
    """Make a request on the short_it endpoint.
       Pass Authorization token from the user that already exists in db"""
    data_json = json.dumps(data)
    headers = {'Content-type': 'application/json',
               'Authorization': 'NyaWDJekdjWI38KejJWlkd93jsdtu'}
    result = requests.post(make_uri("short_it/"),
                           data=data_json,
                           headers=headers)

    return result.json(), result.status_code

