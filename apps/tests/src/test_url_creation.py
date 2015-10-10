from expects import expect, be_a

from yatu.model import ShortUrl
from yatu.handlers import ShortUrlHandler
from .fakes import FakeUnitOfWorkManager, FakeShortifier


class When_a_url_is_shortened_to_a_random_one:

    def given_a_url_a_ShortUrlHandler_and_a_uow(self):
        self.url = "http://www.domain.com/big-article-name-with-params/?q=qwerty&t=10"
        self.uow = FakeUnitOfWorkManager()
        self.shortifier = FakeShortifier(['SID-123'])
        self.handler = ShortUrlHandler(self.uow, self.shortifier)

    def because_we_are_calling_the_handler_to_short_the_url(self):
        self.handler(self.url)

    def it_should_insert_a_short_url(self):

        with self.uow.start() as tx:
            s_url = tx.short_urls.get('SID-123')

        expect(s_url).to(be_a(ShortUrl))

