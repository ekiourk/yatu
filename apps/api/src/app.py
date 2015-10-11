from flask import Flask, Response, json, request
from yatu import bootstrap
from yatu.handlers import ShortUrlHandler

appl = Flask(__name__)

configuration = {
    'postgres_conn_string': "postgres://yatu:@localhost:5432/yatu"
}

bootstrap(configuration)

@appl.route('/short_it/', methods=['POST'])
def short_it():
    json_data = request.json
    handler = ShortUrlHandler()
    sid = handler(json_data.get('url'))
    view = {'success': True,
            'short_url': sid,
            'url': json_data.get('url')}
    resp = Response(json.dumps(view), mimetype="application/json")
    return resp


if __name__ == "__main__":
    appl.run()