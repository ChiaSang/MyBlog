from markupsafe import escape
from flask import Flask, render_template, request, redirect, url_for

from flask_bootstrap import Bootstrap
import settings

from Apps.user.view import user_bp


def create_app():
    #  Set templates path
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    bootstrap = Bootstrap(app)
    #  import flask config file
    app.config.from_object(settings)
    #  blueprint
    app.register_blueprint(user_bp)  # Create a blueprint and bond the blueprint object
    print(app.url_map)
    return app
