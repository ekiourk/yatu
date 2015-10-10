from yatu.model import ShortUrl


class ShortUrlHandler(object):
    def __init__(self, uow=None, shortifier=None):
        self.uow = uow
        self.shortifier = shortifier

    def handle_shorting(self, url):
        sid = self.shortifier(url)
        with self.uow.start() as tx:
            surl = tx.short_urls.get(sid)
            if surl:
                # collision happened
                # TODO: Use a collision specific exception
                raise Exception("Collision")
            surl = ShortUrl(sid, url)
            tx.short_urls.add(surl)


    def __call__(self, url):
        no_of_tries = 10
        while no_of_tries > 0:
            try:
                self.handle_shorting(url)
                return
            except Exception:
                no_of_tries -= 1