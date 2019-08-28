import logging
import os

import werkzeug
from flask import Flask, jsonify, request, has_request_context
from flask.logging import default_handler
from flask_sqlalchemy import SQLAlchemy
from flask_praetorian.exceptions import (
    PraetorianError, MissingUserError, AuthenticationError
)
import flask_cors
from flask_migrate import Migrate
from flask_request_id_header.middleware import RequestID


from app.config import get_config, get_env
from app.error import ApiError

db = SQLAlchemy()
cors = flask_cors.CORS()
migrate = Migrate(compare_type=True)


class RequestFormatter(logging.Formatter):
    def format(self, record):
        record.request_id = 'NA'

        if has_request_context():
            record.request_id = request.environ.get("HTTP_X_REQUEST_ID")

        return super().format(record)


def make_app():
    from app.auth import init_app as init_auth
    from app.api import bp as api_bp
    from app.command import init_command
    app = Flask(__name__)

    app.config.from_pyfile(get_config(), silent=False)
    app.config['SQLALCHEMY_DATABASE_URI'] = get_env(
        'SQLALCHEMY_DATABASE_URI')
    app.config['JWT_ACCESS_LIFESPAN'] = {'hours': 24}
    app.config['JWT_REFRESH_LIFESPAN'] = {'days': 30}
    app.register_error_handler(
        ApiError,
        ApiError.build_error_handler(),
    )

    RequestID(app)
    app.logger.setLevel(os.environ.get('LOG_LEVEL', logging.INFO))
    app.logger.debug('starting application')
    logging.getLogger('werkzeug').disabled = True
    # add unique request id to logger
    formatter = RequestFormatter(
        '[%(asctime)s] [%(levelname)s] [%(request_id)s] %(module)s: %(message)s'
    )
    default_handler.setFormatter(formatter)

    db.init_app(app)
    cors.init_app(app, expose_headers=['x-token'])
    migrate.init_app(app, db)

    init_command(app)
    init_auth(app)
    app.register_blueprint(api_bp)

    @app.errorhandler(werkzeug.exceptions.BadRequest)
    def handle_bad_request(e):
        return 'bad request!', 400

    @app.errorhandler(PraetorianError)
    @app.errorhandler(MissingUserError)
    @app.errorhandler(AuthenticationError)
    def handle_authen_error(e):
        app.logger.warning(e.message)
        return jsonify({
            'status': 401,
            'message': 'Username or password is incorrect'
        }), 200

    return app


app = make_app()
