from expects import expect, have_len, contain
import inject
from .fakes import configure_fake_injects
from yatu.handlers import UrlsForUserHandler
from yatu.model import ShortUrl, User


class When_the_list_of_urls_for_a_user_are_requested:

    def given_some_urls_and_a_user(self):
        configure_fake_injects()

        # Urls for Alice
        self.user = User('Alice')
        short_url1 = ShortUrl('SID-1', "http://url.1", user=self.user)
        short_url2 = ShortUrl('SID-2', "http://url.2", user=self.user)
        self.alice_urls = [short_url1, short_url2]

        # Url for other user
        short_url3 = ShortUrl('SID-3', "http://url.3", user=User('Bob'))

        uow = inject.instance('UnitOfWorkManager')
        uow.sess.short_urls.add(short_url1)
        uow.sess.short_urls.add(short_url2)
        uow.sess.short_urls.add(short_url3)

    def because_the_urls_by_user_are_requested(self):
        self.handler = UrlsForUserHandler(self.user)
        self.result = self.handler()

    def it_should_return_the_urls_only_for_that_user(self):
        expect(self.result).to(have_len(2))
        for item in self.result:
            expect(self.alice_urls).to(contain(item))
