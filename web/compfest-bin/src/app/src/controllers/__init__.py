from flask import render_template
from flask import redirect
from flask import url_for
from flask import request
from flask import session
from flask import flash
from flask import send_file

from .SessionController import login_required
from .SessionController import authorization_required

from .UserController import UserRegisterManager
from .UserController import UserLoginManager
from .UserController import UserManager

from .NoteController import NoteManager
from ..models import Note

import io


@login_required
def index(username):
    notes = NoteManager.get_note_by_current_user()
    user = UserManager.get_user_by_username(username)

    if not user or username != session.get('username'):
        return render_template('404.html')

    return render_template('index.html', username=username, notes=notes)

def login():
    if request.method == 'POST':
        manager = UserLoginManager(request.form)

        if manager.is_user_authorized():
            session['id'] = manager.user.id
            session['username'] = manager.user.username

            return redirect(
                url_for('web.index', username=manager.user.username)
            )

        flash('Username/Password is incorrect!', 'error')
        return redirect(url_for('web.login'))
    
    return render_template('login.html', title='Login')

@login_required
def logout():
    session.clear()

    return redirect(url_for('web.login'))

def register():
    if request.method == 'POST':
        try:
            manager = UserRegisterManager(request.form) 

            if not manager.is_user_existed():
                manager.add_user()

                session['id'] = manager.user.id
                session['username'] = manager.user.username

                return redirect(
                    url_for('web.index', username=manager.user.username)
                )
            else:
                raise Exception('Username already is taken')
        
        except Exception as e:
            flash(str(e), 'error')

        return redirect(url_for('web.register'))

    return render_template('register.html', title='Register')

@login_required
def add_note():
    username = session.get('username')

    if request.method == 'POST':
        manager = NoteManager(request.form)
        manager.add_note()

        return redirect(
            url_for('web.view_note', id=manager.note_id)
        )
    
    return render_template(
        'form.html',
         username=username,
         title='New Note',
    )

@login_required
@authorization_required
def print_note(id):
    user = UserManager.get_user_by_id(session.get('id'))
    note = NoteManager.view_note(id)
    pdf = NoteManager.print_note(note, user)

    return send_file(io.BytesIO(pdf), mimetype='application/pdf')

@login_required
@authorization_required
def view_note(id):
    username = session.get('username')
    note = NoteManager.view_note(id)

    return render_template('note.html', username=username, note=note)

@login_required
@authorization_required
def edit_note(id):
    username = session.get('username')

    if request.method == 'POST':
        manager = NoteManager(request.form)
        manager.edit_note(id)

        return redirect(
            url_for('web.view_note', id=id)
        )
    else:
        note = NoteManager.view_note(id)
        note_title = note.title
        note_content = note.content

    return render_template(
        'form.html',
         username=username,
         title=f'Edit Note: {id}',
         note_title=note_title,
         note_content=note_content
    )

@login_required
@authorization_required
def delete_note(id):
    NoteManager.delete_note(id)
    return redirect(
        url_for('web.index', username=session.get('username'))
    )

@login_required
@authorization_required
def view_raw_note(id):
    note = NoteManager.view_note(id)

    return note.content

@login_required
def edit_profile():
    username = session.get('username')
    fullname = request.form.get('fullname')
    user = UserManager.get_user_by_username(username)

    if request.method == 'POST':
        try:
            UserManager.update_profile(user, fullname)
        except Exception as e:
            flash(str(e))
        else:
            flash('Your settings have been saved!')

        return redirect(
            url_for('web.edit_profile')
        )

    return render_template('profile.html', username=username, user=user)