from expects import expect, equal, be_none
import inject

from yatu.model import ShortUrl
from yatu.handlers import ShortUrlRequestHandler
from .fakes import configure_fake_injects


class When_a_url_that_exists_is_requested:

    def given_a_short_url_in_the_database(self):
        configure_fake_injects()
        self.url = "http://www.domain.com/article/?q=qwerty&t=10"
        self.sid = 'SID-123'
        self.short_url_obj = ShortUrl(self.sid, self.url)
        uow = inject.instance('UnitOfWorkManager')
        uow.sess.short_urls.add(self.short_url_obj)

    def because_we_are_calling_the_handler_to_get_the_original_url(self):
        self.handler = ShortUrlRequestHandler()
        self.result = self.handler(self.sid)

    def it_should_return_the_url(self):
        expect(self.result).to(equal(self.url))

    def it_should_increase_the_visits(self):
        expect(self.short_url_obj.visited_counter).to(equal(1))


class When_a_url_that_does_not_exist_is_requested:

    def given_some_fakes(self):
        configure_fake_injects()

    def because_we_are_calling_the_handler_to_get_the_original_url(self):
        self.handler = ShortUrlRequestHandler()
        self.result = self.handler('SID-THAT-DOESNT-EXIST')

    def it_should_return_the_url(self):
        expect(self.result).to(be_none)
