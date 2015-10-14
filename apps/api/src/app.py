from functools import wraps
from flask import Flask, Response, json, request, abort
import inject

from yatu import bootstrap
from yatu import settings
from yatu.handlers import ShortUrlHandler, SidAlreadyExistsException,\
    ShortUrlRequestHandler, UrlsForUserHandler
from yatu.utils import make_uri

from views import moved_permanently_view, not_found_view, short_urls_list_view,\
    error_500_json_view, short_it_success_view, short_it_collision_view

appl = Flask(__name__)

bootstrap(settings)


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
            return None

        uow = inject.instance('UnitOfWorkManager')
        with uow.start() as tx:
            user = tx.users.get_by_token(request.headers['Authorization'])

        if user is None:
            # Unauthorized
            abort(401)
            return None

        return fn(user=user, *args, **kwargs)
    return _wrap


@appl.route('/short_it/', methods=['POST'])
@authorized
def short_it(user=None):
    json_data = request.json
    url = json_data.get('url')
    short_url = json_data.get('short_url')
    handler = ShortUrlHandler(user)

    try:
        view = short_it_success_view(url, handler(url, short_url))
        return_status = 200
    except SidAlreadyExistsException:
        view = short_it_collision_view(url, short_url)
        return_status = 409
    except Exception as e:
        view = error_500_json_view(str(e))
        return_status = 500

    return Response(json.dumps(view), mimetype="application/json", status=return_status)


@appl.route('/short_urls/', methods=['GET'])
@authorized
def urls_list(user=None):
    handler = UrlsForUserHandler(user)
    try:
        view = short_urls_list_view(handler())
        return_status = 200
    except Exception as e:
        view = error_500_json_view(str(e))
        return_status = 500

    return Response(json.dumps(view), mimetype="application/json", status=return_status)


@appl.route('/<sid>', methods=['GET'])
def go(sid):
    try:
        handler = ShortUrlRequestHandler()
        url = handler(sid)
    except Exception as e:
        #TODO: Show only on debug mode
        return Response(str(e), mimetype="text/html", status=500)

    if url:
        resp = Response(moved_permanently_view(url), mimetype="text/html", status=301)
        resp.headers.add('Location', url)
    else:
        resp = Response(not_found_view(), mimetype="text/html", status=404)

    return resp


if __name__ == "__main__":
    appl.run()
