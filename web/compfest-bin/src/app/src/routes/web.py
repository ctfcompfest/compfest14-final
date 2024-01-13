from flask import render_template
from flask import Blueprint

from ..controllers import index
from ..controllers import login
from ..controllers import logout
from ..controllers import register

from ..controllers import add_note
from ..controllers import print_note
from ..controllers import view_note
from ..controllers import edit_note
from ..controllers import delete_note
from ..controllers import view_raw_note
from ..controllers import edit_profile

web = Blueprint('web', __name__)

@web.app_errorhandler(404)
@web.app_errorhandler(500)
def error_page(e):
    return render_template('404.html'), 404

web.route('/', methods=['GET', 'POST'])(add_note)
web.route('/u/<string:username>', methods=['GET'])(index)
web.route('/login', methods=['GET', 'POST'])(login)
web.route('/logout', methods=['GET'])(logout)
web.route('/signup', methods=['GET', 'POST'])(register)
web.route('/user/profile', methods=['GET', 'POST'])(edit_profile)

web.route('/<string:id>', methods=['GET', 'POST'])(view_note)
web.route('/<string:id>/print', methods=['GET'])(print_note)
web.route('/<string:id>/edit', methods=['GET', 'POST'])(edit_note)
web.route('/<string:id>/delete', methods=['GET'])(delete_note)
web.route('/raw/<string:id>', methods=['GET'])(view_raw_note)