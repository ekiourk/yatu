from expects import expect, equal
import inject
import requests
from retrying import retry

from yatu import bootstrap, settings
from yatu.utils import make_uri
from .context_builders import make_short_it_request

bootstrap(settings)
shortifier = inject.instance('Shortifier')
uow = inject.instance('UnitOfWorkManager')


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

    # Needs to retry because the celery task might be delayed
    @retry(stop_max_attempt_number=7, wait_fixed=100)
    def it_should_increase_the_visits(self):
        with uow.start() as tx:
            short_url = tx.short_urls.get(self.sid)
            expect(short_url.visited_counter).to(equal(1))


class When_a_short_url_that_does_not_exist_is_requested:

    def given_a_short_url_that_is_already_created(self):
        self.short_url = make_uri(shortifier(''))

    def because_we_request_for_the_short_url(self):
        self.result = requests.get(self.short_url, allow_redirects=False)

    def it_should_return_status_code_404(self):
        expect(self.result.status_code).to(equal(404))

