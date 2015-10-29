from functools import wraps
from flask import request, abort
import inject

__author__ = 'ilias'


def authorized(fn):
    """Decorator that checks that requests contain an Authorization header.
    user will be None if the authentication failed,
    and have a user object otherwise.

    Usage:
    @app.route("/")
    @authorized
    def secured_root(user=None):
        pass
    """
    @wraps(fn)
    def _wrap(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)
            return

        uow = inject.instance('UnitOfWorkManager')
        with uow.start() as tx:
            user = tx.users.get_by_token(request.headers['Authorization'])

        if user is None:
            # Unauthorized
            abort(401)
            return

        return fn(user=user, *args, **kwargs)
    return _wrap