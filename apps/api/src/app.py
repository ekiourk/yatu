from flask import Flask, Response, json, request

from yatu import bootstrap
from yatu.handlers import ShortUrlHandler, SidAlreadyExistsException, ShortUrlRequestHandler
from yatu.utils import make_uri

from views import moved_permanently_view, not_found_view

appl = Flask(__name__)

configuration = {
    'postgres_conn_string': "postgres://yatu:@localhost:5432/yatu"
}

bootstrap(configuration)

@appl.route('/short_it/', methods=['POST'])
def short_it():
    json_data = request.json
    url = json_data.get('url')
    short_url = json_data.get('short_url')
    handler = ShortUrlHandler()

    try:
        sid = handler(url, short_url)

        view = {
            'success': True,
            'short_url': make_uri(sid),
            'url': url
        }
        return_status = 200
    except SidAlreadyExistsException:
        view = {
            'success': False,
            'short_message': "Short URL is not available.",
            'error_message': "The url {} is not available. Try another one.".format(make_uri(short_url)),
            'short_url': short_url,
            'url': url
        }
        return_status = 409
    except Exception as e:
        #TODO: Show only on debug mode
        view = {
            'success': False,
            'short_message': "Internal server error",
            'error_message': str(e)
        }
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
