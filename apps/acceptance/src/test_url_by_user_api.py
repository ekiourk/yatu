from datetime import timedelta, datetime
from expects import expect, have_len, equal
import inject
from .context_builders import create_user_with_token, make_user_urls_request
from yatu.model import ShortUrl

from yatu import bootstrap, settings

bootstrap(settings)
shortifier = inject.instance('Shortifier')
uow = inject.instance('UnitOfWorkManager')


class When_the_list_of_urls_for_a_user_are_requested:

    def given_some_urls_and_two_users(self):

        with uow.start() as tx:
            # Urls for Alice
            alice = create_user_with_token(tx)
            self.alice_token = alice.token.token
            self.sid1 = shortifier('url1')
            short_url1 = ShortUrl(self.sid1, "http://url.1", user=alice)
            short_url1.created_at = datetime.now() - timedelta(days=1)
            short_url2 = ShortUrl(shortifier('url2'), "http://url.2", user=alice)
            tx.short_urls.add(short_url1)
            tx.short_urls.add(short_url2)

            # Url for bob
            bob = create_user_with_token(tx)
            self.bob_token = bob.token.token
            short_url3 = ShortUrl(shortifier('url3'), "http://url.3", user=bob)
            tx.short_urls.add(short_url3)

            tx.commit()

    def because_the_urls_by_user_are_requested(self):
        # list requests
        self.result_alice, self.alice_status = make_user_urls_request(self.alice_token)
        self.result_bob, self.bob_status = make_user_urls_request(self.bob_token)

    def it_should_return_the_urls_for_alice_with_status_200(self):
        expect(self.alice_status).to(equal(200))
        expect(self.result_alice).to(have_len(2))
        expect(self.result_alice[0]['url']).to(equal("http://url.2"))
        expect(self.result_alice[1]['url']).to(equal("http://url.1"))

    def it_should_return_the_urls_for_bob_with_status_200(self):
        expect(self.bob_status).to(equal(200))
        expect(self.result_bob).to(have_len(1))
        expect(self.result_bob[0]['url']).to(equal("http://url.3"))

    def it_should_return_one_result_for_specific_sid(self):
        result, status = make_user_urls_request(self.alice_token, self.sid1)
        expect(status).to(equal(200))
        expect(result['url']).to(equal("http://url.1"))

    def it_should_return_404_for_sid_that_does_not_exist(self):
        _, status = make_user_urls_request(self.alice_token, 'sid-do-not-exist')
        expect(status).to(equal(404))

    def it_should_return_403_for_sid_that_does_not_belong_to_user(self):
        _, status = make_user_urls_request(self.bob_token, self.sid1)
        expect(status).to(equal(403))

