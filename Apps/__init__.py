from flask_migrate import Migrate

from markupsafe import escape
from flask import Flask, render_template, request, redirect, url_for

from flask_bootstrap import Bootstrap
import settings

from Apps.user.view import user_bp
from extents import db


def create_app():
    #  Set templates path
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    bootstrap = Bootstrap(app)
    #  import flask config file
    app.config.from_object(settings.DevConfig)
    #  blueprint
    app.register_blueprint(user_bp)  # Create a blueprint and bond the blueprint object
    db.init_app(app=app)
    print(app.url_map)
    return app
