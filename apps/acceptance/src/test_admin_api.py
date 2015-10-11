from expects import expect, equal, have_key, be_a
import json
import requests
from uuid import uuid4

from yatu.utils import make_uri


def make_short_it_request(data):
    data_json = json.dumps(data)
    headers = {'Content-type': 'application/json'}
    result = requests.post(make_uri("short_it/"),
                           data=data_json,
                           headers=headers)
    return result.json()


class When_a_url_shortening_is_requested:

    def given_a_url(self):
        self.url = "http://www.domain.com/big-article-name-with-params/?q=qwerty&t=10"

    def because_we_send_a_shortening_request(self):
        self.result = make_short_it_request({
            "url": self.url
        })

    def it_should_return_an_sid(self):
        expect(self.result).to(have_key('short_url'))
        short_url = self.result['short_url']
        expect(short_url).to(be_a(str))
        expect(self.result).to(equal({'success': True, 'short_url': short_url, 'url': self.url}))


class When_a_url_shortening_is_requested_with_a_predefined_short_version:

    def given_a_url_and_a_short_url(self):
        self.url = "http://www.domain.com/big-article-name-with-params/?q=qwerty&t=10"
        self.short_url = str(uuid4())

    def because_we_send_a_shortening_request(self):
        self.result = make_short_it_request({
            "url": self.url,
            "short_url": self.short_url
        })

    def it_should_return_an_sid(self):
        expect(self.result).to(equal({'success': True, 'short_url': make_uri(self.short_url), 'url': self.url}))