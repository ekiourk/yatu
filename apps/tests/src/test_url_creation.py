from expects import expect, be_a



class FakeRepository:

    def __init__(self):
        self.items = []

    def add(self, url):
        self.items.append(url)

    def get(self, sid):
        raise NotImplementedError("get")


class FakeShortUrlRepository(FakeRepository):

    def get(self, sid):
        for item in self.items:
            if item.sid == sid:
                return item


class FakeUnitOfWork:

    def __init__(self):
        self.short_urls = FakeShortUrlRepository()
        self.committed = False
        self.rolled_back = False

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def commit(self):
        self.committed = True

    def rollback(self):
        self.rolled_back = True


class FakeUnitOfWorkManager:

    def __init__(self):
        self.sess = FakeUnitOfWork()

    def start(self):
        return self.sess

    @property
    def short_urls(self):
        return self.sess.short_urls


class ShortUrl:
    def __init__(self, sid, url):
        self.sid = sid
        self.url = url


class ShortUrlHandler(object):
    def __init__(self, uow=None, shortifier=None):
        self.uow = uow
        self.shortifier = shortifier

    def __call__(self, url):
        sid = self.shortifier(url)
        with self.uow.start() as tx:
            surl = tx.short_urls.get(sid)
            if surl is None:
                surl = ShortUrl(sid, url)
                tx.short_urls.add(surl)


class FakeShortifier:
    def __init__(self, results):
        self.results = results

    def __call__(self, url):
        try:
            return self.results.pop(0)
        except IndexError:
            return


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

