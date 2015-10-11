from expects import expect, be_a, equal, raise_error

from yatu.model import ShortUrl
from yatu.handlers import ShortUrlHandler, SidAlreadyExistsException
from .fakes import FakeUnitOfWorkManager, FakeShortifier


class When_a_url_is_shortened_to_an_auto_generated_one:

    def given_a_url_a_ShortUrlHandler_and_a_uow(self):
        self.url = "http://www.domain.com/big-article-name-with-params/?q=qwerty&t=10"
        self.uow = FakeUnitOfWorkManager()
        self.shortifier = FakeShortifier(['SID-123'])
        self.handler = ShortUrlHandler(self.uow, self.shortifier)

    def because_we_are_calling_the_handler_to_short_the_url(self):
        self.sid = self.handler(self.url)

    def it_should_return_the_sid(self):
        expect(self.sid).to(equal('SID-123'))

    def it_should_insert_a_short_url(self):
        with self.uow.start() as tx:
            s_url = tx.short_urls.get('SID-123')

        expect(s_url).to(be_a(ShortUrl))
        expect(s_url.url).to(equal(self.url))


class When_two_different_urls_are_shortened_and_a_colision_occurs:

    def given_two_urls_and_a_shortifier_that_returns_the_same_cid(self):
        self.url1 = "http://www.domain.com/big-article-name-with-params/?q=qwerty&t=10"
        self.url2 = "http://www.anotherdomain.com/article/?p=10"
        self.uow = FakeUnitOfWorkManager()
        self.shortifier = FakeShortifier(['SID-123', 'SID-123', 'SID-321'])
        self.handler = ShortUrlHandler(self.uow, self.shortifier)

    def because_we_are_calling_the_handler_to_short_the_first_url(self):
        self.handler(self.url1)
        self.handler(self.url2)

    def it_should_handle_the_collison_and_insert_both_urls(self):
        with self.uow.start() as tx:
            s_url1 = tx.short_urls.get('SID-123')
            s_url2 = tx.short_urls.get('SID-321')

        expect(s_url1.url).to(equal(self.url1))
        expect(s_url2.url).to(equal(self.url2))


class When_the_same_url_is_shortened_twice_and_results_on_the_same_sid:

    def given_a_url_and_a_shortifier(self):
        self.url = "http://www.domain.com/big-article-name-with-params/?q=qwerty&t=10"
        self.uow = FakeUnitOfWorkManager()
        self.shortifier = FakeShortifier(['SID-123', 'SID-123', 'SID-321'])
        self.handler = ShortUrlHandler(self.uow, self.shortifier)

    def because_we_are_calling_the_handler_to_short_the_first_url(self):
        self.handler(self.url)
        self.handler(self.url)

    def it_should_handle_the_collison_and_insert_the_url_twice(self):
        with self.uow.start() as tx:
            s_url1 = tx.short_urls.get('SID-123')
            s_url2 = tx.short_urls.get('SID-321')

        expect(s_url1.url).to(equal(self.url))
        expect(s_url2.url).to(equal(self.url))


class When_a_url_is_shortened_to_a_given_sid:

    def given_a_url_a_ShortUrlHandler_and_a_uow(self):
        self.url = "http://www.domain.com/big-article-name-with-params/?q=qwerty&t=10"
        self.given_sid = "5Y14wQ"
        self.uow = FakeUnitOfWorkManager()
        self.handler = ShortUrlHandler(self.uow, FakeShortifier())

    def because_we_are_calling_the_handler_to_short_the_url(self):
        self.handler(self.url, self.given_sid)

    def it_should_insert_a_short_url(self):
        with self.uow.start() as tx:
            s_url = tx.short_urls.get(self.given_sid)

        expect(s_url).to(be_a(ShortUrl))
        expect(s_url.url).to(equal(self.url))


class When_a_url_is_shortened_to_a_given_by_the_user_sid_but_sid_already_exists:

    def given_a_short_url_already_stored(self):
        self.url = "http://www.domain.com/big-article-name-with-params/?q=qwerty&t=10"
        self.given_sid = "5Y14wQ"
        self.uow = FakeUnitOfWorkManager()
        self.handler = ShortUrlHandler(self.uow, FakeShortifier())
        self.uow.sess.short_urls.add(ShortUrl(self.given_sid, "http://a_url.com/"))

    def because_we_are_calling_the_handler_to_short_the_url(self):
        self.callback = lambda: self.handler(self.url, self.given_sid)

    def it_should_raise_an_error(self):
        expect(self.callback).to(raise_error(SidAlreadyExistsException))
