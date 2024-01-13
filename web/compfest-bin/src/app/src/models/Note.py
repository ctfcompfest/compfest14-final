from sqlalchemy.orm import validates
from random import choice

from . import db
from html import escape

import string

CHARSET = string.ascii_letters + string.digits
DEFAULT_TITLE = 'Untitled'
DEFAULT_CONTENT = ''


def rand_id():
    return ''.join(choice(CHARSET) for x in range(8))


class Note(db.Model):
    __tablename__ = 'notes'
    __table_args__ = dict(sqlite_autoincrement=True)

    id = db.Column(db.String(36), primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    content = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.String(32), db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    modified_at = db.Column(db.DateTime, nullable=False, default=db.func.now(), onupdate=db.func.now())

    def __init__(self, title, content, user_id, note_id=None, created_at=None, modified_at=None):
        self.id = note_id or rand_id()
        self.title = title or DEFAULT_TITLE
        self.content = content or DEFAULT_CONTENT
        self.user_id = user_id

        self.created_at = self.created_at or created_at
        self.modified_at = self.modified_at or modified_at
    
    @validates("content")
    def validate_content(self, key, value):
        return escape(value)