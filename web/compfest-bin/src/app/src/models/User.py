from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from sqlalchemy.orm import validates

from . import db

import uuid

USERNAME_MAX_LENGTH = 30
FULLNAME_MAX_LENGTH = 100

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(36), primary_key=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(94), nullable=False)
    fullname = db.Column(db.String(64), nullable=False)

    def __init__(self, username, password):
        self.id = str(uuid.uuid4())
        self.username = username
        self.password = generate_password_hash(password)
        self.fullname = username

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def verify_uniqueness(self):
        return self.query.filter_by(username=self.username).first()

    @validates("username")
    def limit_username(self, key, value):
        if len(value) > USERNAME_MAX_LENGTH:
            raise Exception('Username length should not exceeds 30 character')

        return value

    @validates("fullname")
    def limit_fullname(self, key, value):
        if len(value) > FULLNAME_MAX_LENGTH:
            raise Exception('Fullname length should not exceeds 120 character')
        
        return value
