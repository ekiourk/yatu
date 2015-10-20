import inject

from yatu.exceptions import ShortUrlNotFound, ShortUrlInfoForbidden, SidCollisionException, SidAlreadyExistsException
from yatu.model import ShortUrl
from yatu.tasks import increase_visits_count


class ShortUrlHandler:
    @inject.params(uow='UnitOfWorkManager', shortifier='Shortifier')
    def __init__(self, user, uow=None, shortifier=None):
        self.uow = uow
        self.shortifier = shortifier
        self.user = user

    def handle_shorting(self, url, given_sid):
        sid = given_sid or self.shortifier(url)
        with self.uow.start() as tx:
            surl = tx.short_urls.get(sid)
            if surl:
                # collision happened
                raise SidCollisionException("Collision")
            surl = ShortUrl(sid, url)
            surl.user = self.user
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
        result = None
        with self.uow.start() as tx:
            short_url = tx.short_urls.get(sid)
            if short_url:
                result = short_url.url
        if result:
            increase_visits_count.delay(sid)
        return result


class UrlsForUserHandler:
    """Handler to return a list of ShortUrls for a given user"""
    @inject.params(uow='UnitOfWorkManager')
    def __init__(self, user, uow=None):
        self.uow = uow
        self.user = user

    def __call__(self):
        #TODO: Support pagination
        with self.uow.start() as tx:
            return tx.short_urls.get_by_user(self.user)


class UrlInfoRequestHandler:
    """Handler to return a list of ShortUrls for a given user"""
    @inject.params(uow='UnitOfWorkManager')
    def __init__(self, user, uow=None):
        self.uow = uow
        self.user = user

    def __call__(self, sid):
        with self.uow.start() as tx:
            short_url = tx.short_urls.get(sid)
            if short_url:
                if short_url.user == self.user:
                    return short_url
                raise ShortUrlInfoForbidden()
            raise ShortUrlNotFound()

