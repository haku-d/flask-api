from .db import init_command as db_init_command


def init_command(app):
    db_init_command(app)
