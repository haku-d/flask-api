import werkzeug
import flask_buzz
from flask import jsonify


class Error(Exception):
    """Base error for this module."""
    pass


class ApiError(flask_buzz.FlaskBuzz):
    status_code = 200
    response_code = 400

    def jsonify(self):

        if self.response_code is None:
            self.response_code = self.status_code

        return jsonify({
            'status': self.response_code,
            'error': repr(self),
            'message': self.message,
        })


class InvalidRegisteredUserError(ApiError):
    """Invalid email or password"""
    pass


class VerifyRegistrationError(ApiError):
    pass


class BadRequest(ApiError):
    pass


class InvalidRequestError(werkzeug.exceptions.HTTPException):
    response_code = 400
    description = 'Bad request'


class HttpError(Error):
    def __init__(self, status_code):
        self.status_code = status_code
        Error.__init__(self,
                       'HttpError with status code: %s' % self.status_code)


class DbExceptionError(Error):
    pass
