from flask import jsonify
from . import api

def error_response(e):
    response = jsonify({'error': e.name})
    response.status_code = e.code
    return response


@api.app_errorhandler(404)
def page_not_found(e):
    return error_response(e)


@api.app_errorhandler(500)
def internal_server_error(e):
    return error_response(e)
