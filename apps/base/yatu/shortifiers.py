import uuid


class UUIDShortifier:

    def __call__(self, url):
        #TODO: create something better than that
        unique_id = str(uuid.uuid3(uuid.uuid1(), url))
        return unique_id.split('-')[0]