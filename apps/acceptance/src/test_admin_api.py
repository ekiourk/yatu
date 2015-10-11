import json
from urllib.parse import urljoin

from expects import expect, equal, have_key, be_a
import requests


def make_uri(path):
    return urljoin('http://localhost:8080', path)


class When_a_url_shortening_is_requested:

    def given_a_url(self):
        self.url = "http://www.domain.com/big-article-name-with-params/?q=qwerty&t=10"

    def because_we_send_a_shortening_request(self):
        data_json = json.dumps({
            "url": self.url
        })
        headers = {'Content-type': 'application/json'}
        result = requests.post(make_uri("short_it/"),
                          data=data_json,
                          headers=headers)

        self.result = result.json()

    def it_should_return_an_sid(self):
        expect(self.result).to(have_key('short_url'))
        short_url = self.result['short_url']
        expect(short_url).to(be_a(str))
        expect(self.result).to(equal({'success': True, 'short_url': short_url, 'url': self.url}))