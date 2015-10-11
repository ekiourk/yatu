import inject

from yatu.model import ShortUrl


class SidCollisionException(Exception):
    pass


class SidAlreadyExistsException(Exception):
    pass


class ShortUrlHandler:
    @inject.params(uow='UnitOfWorkManager', shortifier='Shortifier')
    def __init__(self, uow=None, shortifier=None):
        self.uow = uow
        self.shortifier = shortifier

    def handle_shorting(self, url, given_sid):
        sid = given_sid or self.shortifier(url)
        with self.uow.start() as tx:
            surl = tx.short_urls.get(sid)
            if surl:
                # collision happened
                raise SidCollisionException("Collision")
            surl = ShortUrl(sid, url)
            tx.short_urls.add(surl)
            tx.commit()
        return sid

    def __call__(self, url, given_sid=None):
        no_of_tries = 10
        while no_of_tries > 0:
            try:
                return self.handle_shorting(url, given_sid)
            except SidCollisionException:
                if given_sid:
                    raise SidAlreadyExistsException()
                no_of_tries -= 1


class ShortUrlRequestHandler:
    @inject.params(uow='UnitOfWorkManager')
    def __init__(self, uow=None):
        self.uow = uow

    def __call__(self, sid):
        with self.uow.start() as tx:
            short_url = tx.short_urls.get(sid)
            if short_url:
                return short_url.url

