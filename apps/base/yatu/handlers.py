from yatu.model import ShortUrl


class ShortUrlHandler(object):
    def __init__(self, uow=None, shortifier=None):
        self.uow = uow
        self.shortifier = shortifier

    def handle_shorting(self, url, given_sid):
        sid = given_sid or self.shortifier(url)
        with self.uow.start() as tx:
            surl = tx.short_urls.get(sid)
            if surl:
                # collision happened
                # TODO: Use a collision specific exception
                raise Exception("Collision")
            surl = ShortUrl(sid, url)
            tx.short_urls.add(surl)


    def __call__(self, url, given_sid=None):
        no_of_tries = 10
        while no_of_tries > 0:
            try:
                self.handle_shorting(url, given_sid)
                return
            except Exception:
                if given_sid:
                    raise
                no_of_tries -= 1