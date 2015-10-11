from expects import expect, equal
import requests

from yatu.shortifiers import UUIDShortifier
from yatu.utils import make_uri
from .context_builders import make_short_it_request

shortifier = UUIDShortifier()


class When_a_short_url_is_requested:

    def given_a_short_url_that_is_already_created(self):
        self.url = "http://www.domain.com/big-article-name-with-params/?q=qwerty&t=10"
        self.sid = shortifier(self.url)
        self.short_url = make_uri(self.sid)

        make_short_it_request({
            "url": self.url,
            "short_url": self.sid
        })

    def because_we_request_for_the_short_url(self):
        self.result = requests.get(self.short_url, allow_redirects=False)

    def it_should_return_status_code_301(self):
        expect(self.result.status_code).to(equal(301))

    def it_should_redirect_to_the_original_url(self):
        expect(self.result.headers.get('location')).to(equal(self.url))


class When_a_short_url_that_does_not_exist_is_requested:

    def given_a_short_url_that_is_already_created(self):
        self.short_url = make_uri(shortifier(''))

    def because_we_request_for_the_short_url(self):
        self.result = requests.get(self.short_url, allow_redirects=False)

    def it_should_return_status_code_404(self):
        expect(self.result.status_code).to(equal(404))

