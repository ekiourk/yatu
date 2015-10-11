import uuid


class UUIDShortifier:

    def __call__(self, url):
        #TODO: create something better than that
        return str(uuid.uuid3(uuid.uuid1(), url))