
class ShortUrlNotFound(Exception):
    pass


class ShortUrlInfoForbidden(Exception):
    pass


class SidCollisionException(Exception):
    pass


class SidAlreadyExistsException(Exception):
    pass