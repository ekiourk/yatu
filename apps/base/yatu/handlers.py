from yatu.model import ShortUrl


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