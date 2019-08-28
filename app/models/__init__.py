import re
from datetime import datetime, timedelta
from sqlalchemy.dialects.mssql import TINYINT
from app import db
from app.utils.generator import gen_hash_key


class TimestampMixin(object):
    created_date = db.Column(
        db.DateTime, nullable=True, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, onupdate=datetime.utcnow)
    deleted_date = db.Column(db.DateTime, nullable=True, default=None)

    def update(self, b):
        for key, value in b.items():
            setattr(self, key, value)


class User(TimestampMixin, db.Model):
    __tablename__ = 'users'

    ACTIVE_STATUS = 1
    INACTIVE_STATUS = 0

    next30min = datetime.now() + timedelta(minutes=30)

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    is_active = db.Column(TINYINT,
                          nullable=False, default=False)
    email = db.Column(db.String(100), nullable=True, unique=True)
    website = db.Column(db.String(255), nullable=True)
    password = db.Column(db.String(255), nullable=False)
    facebook = db.Column(db.String(255), nullable=True)
    email_confirmed_at = db.Column(db.DateTime, nullable=True)
    active_code = db.Column(
        db.String(128), nullable=True, default=gen_hash_key())
    active_code_expired_at = db.Column(
        db.Integer, nullable=True, default=next30min.timestamp())

    # User information
    roles = db.Column(db.Text)

    __table_args__ = (
        db.Index('idx_email', email),
    )

    @property
    def rolenames(self):
        try:
            return self.roles.split(',')
        except Exception:
            return []

    @classmethod
    def lookup(cls, email):
        return cls.query.filter_by(email=email).one_or_none()

    @classmethod
    def identify(cls, id):
        return cls.query.get(id)

    @property
    def identity(self):
        return self.id

    def is_valid(self):
        return self.is_active

    @property
    def is_admin(self):
        return 'admin' in self.rolenames

    @property
    def is_user(self):
        return 'user' in self.rolenames

    def has_role(self, role):
        return role in self.rolenames

    @classmethod
    def is_valid_email(cls, email):
        email = email.strip()
        reg = re.compile(
            "^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$", re.I)
        match = reg.match(email)
        return True if match else False

    @classmethod
    def is_valid_password(cls, password):
        password = password.strip()
        return False if len(password) == 0 else True

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'facebook': self.facebook,
            'website': self.website,
            'is_active': self.is_active,
            'created_date': self.created_date
        }


class UserToken(TimestampMixin, db.Model):
    __tablename__ = 'user_tokens'

    ACTIVE_STATUS = 1
    REVOKED_STATUS = 2

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    token = db.Column(db.String(128), nullable=False)
    status = db.Column(db.Integer, default=ACTIVE_STATUS)
    logged_datetime = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)
    updated_date = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @classmethod
    def is_revoked(cls, token):
        token = cls.query.filter_by(
            token=token, status=cls.REVOKED_STATUS).one_or_none()
        return False if token is None else True
