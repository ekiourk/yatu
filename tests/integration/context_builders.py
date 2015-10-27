import json
from uuid import uuid4
import requests

from yatu.model import User, AccessToken
from yatu.utils import make_uri


def make_short_it_request(data):
    """Make a request on the short_it endpoint.
       Pass Authorization token from the user that already exists in db"""
    data_json = json.dumps(data)
    headers = {'Content-type': 'application/json',
               'Authorization': 'NyaWDJekdjWI38KejJWlkd93jsdtu'}
    result = requests.post(
        make_uri("short_it/"),
        data=data_json,
        headers=headers
    )

    return result.json(), result.status_code


def make_user_urls_request(token, sid=''):
    headers = {'Content-type': 'application/json',
               'Authorization': token}
    result = requests.get(
        make_uri("short_urls/{}".format(sid)),
        headers=headers
    )

    return result.json(), result.status_code


def create_user_with_token(tx):
    uid = str(uuid4()).split('-')[0]
    user = User('User'+uid)
    user.email = 'email'+uid
    user.password = 'pass'+uid
    user.token = AccessToken(token='token'+uid)
    tx.users.add(user)
    return user