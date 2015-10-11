from flask import Flask, Response, json, request
from yatu import bootstrap
from yatu.handlers import ShortUrlHandler, SidAlreadyExistsException
from yatu.utils import make_uri

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

    resp = Response(json.dumps(view), mimetype="application/json", status=return_status)
    return resp


if __name__ == "__main__":
    appl.run()