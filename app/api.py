from os import environ as env
from flask import Blueprint, jsonify, request, make_response


bp = Blueprint('api', __name__, url_prefix='/api')

API_KEY_LENGTH = 20
MASTER_PW = env.get('MASTER_PW', '')


def api_response(data, status=200, headers=None):
    body = {
        'status': status,
        'data': data
    }
    response = make_response(jsonify(body))
    if headers is not None:
        for key, value in headers.items():
            response.headers[key] = value

    return response


def is_valid_api_key(api_key):
    if api_key is None:
        return False
    if len(api_key) != API_KEY_LENGTH:
        return False

    return True


def my_response(body):
    if not body:
        body = {
            'status': 'ERROR',
        }

    body['request_id'] = request.environ.get("HTTP_X_REQUEST_ID")

    return jsonify(body)


def get_request_data(keys):
    req = request.get_json(force=True)
    data = {}
    for key in keys:
        if key in req:
            data[key] = req.get(key, None)
    return data


@bp.route('/', methods=['GET'])
def index():
    return api_response({'msg': 'Hello world'})
