from expects import expect, equal, be_none

from yatu.model import ShortUrl
from yatu.handlers import ShortUrlRequestHandler
from .fakes import FakeUnitOfWorkManager


class When_a_url_that_exists_is_requested:

    def given_a_short_url_in_the_database(self):
        self.url = "http://www.domain.com/article/?q=qwerty&t=10"
        self.sid = 'SID-123'
        self.uow = FakeUnitOfWorkManager()
        short_url_obj = ShortUrl(self.sid, self.url)
        self.uow.sess.short_urls.add(short_url_obj)

    def because_we_are_calling_the_handler_to_get_the_original_url(self):
        self.handler = ShortUrlRequestHandler(uow=self.uow)
        self.result = self.handler(self.sid)

    def it_should_return_the_url(self):
        expect(self.result).to(equal(self.url))


class When_a_url_that_does_not_exist_is_requested:

    def given_a_short_url_in_the_database(self):
        self.uow = FakeUnitOfWorkManager()

    def because_we_are_calling_the_handler_to_get_the_original_url(self):
        self.handler = ShortUrlRequestHandler(uow=self.uow)
        self.result = self.handler('SID-THAT-DOESNT-EXIST')

    def it_should_return_the_url(self):
        expect(self.result).to(be_none)
