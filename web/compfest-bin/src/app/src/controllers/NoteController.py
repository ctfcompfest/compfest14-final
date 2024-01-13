from flask import session
from flask import request
from flask import render_template

from weasyprint import HTML

from ..models.Note import Note
from ..models import db

from .UserController import UserManager
from .Utils import encrypt
from .Utils import decrypt


class NoteManager(object):
    def __init__(self, body):
        self.title = body.get('title')
        self.content = body.get('content')
        self.user_id = session.get('id')
        self.note = Note(
            self.title,
            encrypt(self.content, session),
            self.user_id
        )

    def add_note(self):
        db.session.add(self.note)
        db.session.commit()

    def edit_note(self, note_id):
        note = NoteManager.get_note_by_id(note_id)
        note.title = self.title
        note.content = encrypt(self.content, session)

        db.session.commit()

    @staticmethod
    def print_note(note, user):
        template_string = render_template(
            'publish.html',
             fullname=user.fullname,
             note=note,
        )

        return HTML(string=template_string).write_pdf()

    @staticmethod
    def view_note(id):
        note = NoteManager.get_note_by_id(id)
        decrypted_data = decrypt(note.content, session, note.modified_at)

        return Note(
            note.title, decrypted_data, session.get('id'),
            note_id=note.id, created_at=note.created_at, modified_at=note.modified_at
        )

    @staticmethod
    def delete_note(note_id):
        note = NoteManager.get_note_by_id(note_id)
        
        db.session.delete(note)
        db.session.commit()

    @staticmethod
    def get_note_by_current_user():
        return Note.query.filter_by(
            user_id=session.get('id')
        ).all()

    @staticmethod
    def get_note_by_id(note_id):
        return Note.query.filter_by(id=note_id).first()

    @staticmethod
    def is_eligible(note_id, user_id):
        note = Note.query.filter_by(
            id=note_id,
            user_id=user_id
        ).first()

        if note:
            return True

        return False

    @property
    def note_id(self):
        return self.note.id