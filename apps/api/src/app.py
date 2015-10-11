from flask import Flask, Response, json, request

appl = Flask(__name__)


@appl.route('/short_it/', methods=['POST'])
def short_it():
    json_data = request.json
    view = {'success': True,
            'short_url': "",
            'url': json_data.get('url')}
    resp = Response(json.dumps(view), mimetype="application/json")
    return resp


if __name__ == "__main__":
    appl.run()