from expects import expect, equal, have_key, be_a
from uuid import uuid4

from .context_builders import make_short_it_request
from yatu.utils import make_uri


class When_a_url_shortening_is_requested:

    def given_a_url(self):
        self.url = "http://www.domain.com/big-article-name-with-params/?q=qwerty&t=10"

    def because_we_send_a_shortening_request(self):
        self.result, self.status_code = make_short_it_request({
            "url": self.url
        })

    def it_should_return_status_code_200(self):
        expect(self.status_code).to(equal(200))

    def it_should_return_an_sid(self):
        expect(self.result).to(have_key('short_url'))
        short_url = self.result['short_url']
        expect(short_url).to(be_a(str))
        expect(self.result).to(equal({
            'success': True,
            'short_url': short_url,
            'url': self.url
        }))


class When_a_url_shortening_is_requested_with_a_predefined_short_version:

    def given_a_url_and_a_short_url(self):
        self.url = "http://www.domain.com/big-article-name-with-params/?q=qwerty&t=10"
        self.short_url = str(uuid4())

    def because_we_send_a_shortening_request(self):
        self.result, self.status_code = make_short_it_request({
            "url": self.url,
            "short_url": self.short_url
        })

    def it_should_return_status_code_200(self):
        expect(self.status_code).to(equal(200))

    def it_should_return_an_sid(self):
        expect(self.result).to(equal({
            'success': True,
            'short_url': make_uri(self.short_url),
            'url': self.url
        }))


class When_a_url_shortening_is_requested_with_a_predefined_short_version_that_is_already_used:

    def given_a_url_and_a_short_url(self):
        self.url = "http://www.domain.com/big-article-name-with-params/?q=qwerty&t=10"
        self.short_url = str(uuid4())

    def because_we_send_a_shortening_request_twice(self):
        make_short_it_request({
            "url": self.url,
            "short_url": self.short_url
        })
        self.result, self.status_code = make_short_it_request({
            "url": self.url,
            "short_url": self.short_url
        })

    def the_second_request_it_should_return_status_code_409(self):
        expect(self.status_code).to(equal(409))

    def the_second_request_it_should_return_an_error(self):
        expect(self.result).to(equal({
            'success': False,
            'short_message': "Short URL is not available.",
            'error_message': "The url {} is not available. Try another one.".format(make_uri(self.short_url)),
            'short_url': self.short_url,
            'url': self.url
        }))