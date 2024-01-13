from flask import session
from flask import redirect
from flask import url_for
from flask import request
from flask import flash

from functools import wraps

from .UserController import UserManager
from .NoteController import NoteManager


def return_on_failure(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            return

    return wrapped

def login_required(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        manager = SessionManager()

        if not manager.is_user_authenticated():
            return redirect(url_for('web.login'))

        return f(*args, **kwargs)

    return wrapped

def authorization_required(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        manager = SessionManager()
        note_id = kwargs.get('id')
        username = manager.username

        if not manager.is_user_authorized(note_id):
            flash('Not enough permission to access this note', 'error')

            return redirect(url_for('web.index', username=username))

        return f(*args, **kwargs)

    return wrapped


class SessionManager(object):
    def __init__(self):
        self.id = session.get('id')
        self.username = session.get('username')

    @return_on_failure
    def is_user_authenticated(self):
        return UserManager.is_eligible(self.username, self.id)

    @return_on_failure
    def is_user_authorized(self, note_id):
        return NoteManager.is_eligible(note_id, self.id)