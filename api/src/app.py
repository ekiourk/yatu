from flask import Flask, Response, request, jsonify, render_template

from decorators import authorized
from yatu import bootstrap
from yatu import settings
from yatu.exceptions import ShortUrlNotFound, ShortUrlInfoForbidden
from yatu.handlers import ShortUrlHandler, SidAlreadyExistsException,\
    ShortUrlRequestHandler, UrlsForUserHandler, UrlInfoRequestHandler
from views import short_urls_list_view, error_500_view,\
    short_it_success_view, short_it_collision_view, short_url_single_view,\
    not_found_404_view, forbidden_found_403_view


appl = Flask(__name__)

bootstrap(settings)


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
        view = error_500_view(str(e))
        return_status = 500

    response = jsonify(view)
    response.status_code = return_status
    return response


@appl.route('/short_urls/', methods=['GET'])
@authorized
def short_urls_list(user=None):
    try:
        handler = UrlsForUserHandler(user)
        view = short_urls_list_view(handler())
        return_status = 200
    except Exception as e:
        view = error_500_view(str(e))
        return_status = 500

    response = jsonify(view)
    response.status_code = return_status
    return response


@appl.route('/short_urls/<sid>', methods=['GET'])
@authorized
def short_url(user=None, sid=None):
    try:
        handler = UrlInfoRequestHandler(user)
        view = short_url_single_view(handler(sid))
        return_status = 200
    except ShortUrlNotFound:
        view = not_found_404_view('Short url {} not found'.format(sid))
        return_status = 404
    except ShortUrlInfoForbidden:
        view = forbidden_found_403_view('Not allowed to access short url {}'.format(sid))
        return_status = 403
    except Exception as e:
        view = error_500_view(str(e))
        return_status = 500

    response = jsonify(view)
    response.status_code = return_status
    return response


@appl.route('/<sid>', methods=['GET'])
def go(sid):
    try:
        handler = ShortUrlRequestHandler()
        url = handler(sid)
    except Exception as e:
        #TODO: Show only on debug mode
        return Response(str(e), mimetype="text/html", status=500)

    if url:
        resp = Response(
            render_template('url_moved_permanently.html', url=url),
            mimetype="text/html",
            status=301
        )
        resp.headers.add('Location', url)
    else:
        resp = Response(
            render_template('url_not_found.html'),
            mimetype="text/html",
            status=404
        )

    return resp


if __name__ == "__main__":
    appl.run()
