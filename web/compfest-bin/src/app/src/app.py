from flask_wtf.csrf import CSRFProtect
from flask import render_template
from flask import Flask

from .models import migrate
from .models import db
from .routes import web
from .routes import api

from .config import AppConfig

import babel

def initialize(app):
    db.init_app(app)
    
    migrate.init_app(app, db)
    app.register_blueprint(web)
    app.register_blueprint(api)

    csrf.init_app(app)

csrf = CSRFProtect()
app = Flask(__name__)
app.config.from_object(AppConfig)

@app.template_filter('strftime')
def _jinja2_filter_datetime(value, format="medium"):
    if format == 'full':
        format="EEEE, d. MMMM y 'at' HH:mm"
    elif format == 'medium':
        format="EE, dd.MM.y HH:mm"
    return babel.dates.format_datetime(value, format)

initialize(app)
