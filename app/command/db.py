import click

from sqlalchemy.exc import SQLAlchemyError
from flask import current_app
from flask.cli import with_appcontext
from app import db
from app.models import User
from app.auth import guard


DAY = 3600 * 24


@click.command('init-db')
@with_appcontext
def init_db():
    # Reflect all tables from database
    db.reflect()
    # Try to drop all tables
    db.drop_all()
    # Re-initiate all tables
    db.create_all()
    click.echo('Initialized the database.')


@click.command('create-user')
@click.argument('email')
@click.argument('password')
@click.option('--role', default='user', help='Specific user role')
@with_appcontext
def create_user(email, password, role):
    try:
        click.echo('Adding new user...')
        user = User(
            email=email,
            is_active=True,
            password=guard.encrypt_password(password),
            roles=role
        )
        db.session.add(user)
        # commit because i need user.id
        db.session.commit()
        """
        Echo user information
        """
        click.echo('New user {} was registered successfully!'.format(user.id))
        db.session.commit()
    except SQLAlchemyError as exc:
        current_app.logger.error(exc)
        db.session.rollback()


@click.command('change-password')
@click.argument('user_id')
@click.argument('password')
@with_appcontext
def change_password(user_id, password):
    try:
        User.query.filter_by(id=user_id).update({'password': password})
        db.session.commit()
    except SQLAlchemyError as err:
        current_app.logger.error(err)
        db.session.rollback()
        click.echo('Error: could not change user password')


def init_command(app):
    app.cli.add_command(init_db)
    app.cli.add_command(create_user)
    app.cli.add_command(change_password)
