import os


def get_config():
    env = os.environ.get('FLASK_ENV', default='development')
    return 'config/%s.config.cfg' % ('dev' if env ==
                                     'development' else 'prod')


def get_db_uri():
    return get_env('SQLALCHEMY_DATABASE_URI')


def get_celery_broker_uri():
    return get_env('CELERY_BROKER_URL')


def get_amqp_broker_url():
    return get_env('AMQP_BROKER_URL')


def get_env(key, required=True):
    env = os.environ.get(key, None)

    if required and not env:
        raise ValueError(f'{key} is required')

    return env


__all__ = [
    'get_config',
    'get_env'
]
