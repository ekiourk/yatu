import inject


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

    def get_by_user(self, user):
        result = []
        for item in self.items:
            if item.user == user:
                result.append(item)

        return result


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


class FakeShortifier:
    def __init__(self, results=None):
        self.results = results or []

    def __call__(self, url):
        try:
            return self.results.pop(0)
        except IndexError:
            return


def configure_fake_injects(uow=None, shortifier=None):
    inject.clear_and_configure(
        lambda binder: binder.bind(
            'UnitOfWorkManager', uow or FakeUnitOfWorkManager()
        ).bind(
            'Shortifier', shortifier or FakeShortifier()
        )
    )
