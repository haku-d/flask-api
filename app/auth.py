import functools
from os import environ as env
import flask_praetorian
from flask import request
from app.error import ApiError

from app.models import User, UserToken

MASTER_PW = env.get('MASTER_PW', '')
guard = flask_praetorian.Praetorian()


def is_blacklisted(token):
    return UserToken.is_revoked(token)


def internal_authenticated():
    header_key = 'x-internal-token'
    header = request.headers.get(header_key, None)

    return True if header == MASTER_PW else False


def internal_authentication_required(func):
    @functools.wraps(func)
    def authenticate(*args, **kwargs):
        ApiError.require_condition(internal_authenticated(), 'access denied')
        return func(*args, **kwargs)
    return authenticate


def init_app(app):
    # Initialize the flask-praetorian instance for the app
    guard.init_app(app, User, is_blacklisted=is_blacklisted)
