from flask import Flask, redirect, url_for

# from flask_bootstrap import Bootstrap
import settings
from Apps.article.view import article_bp
from Apps.user.model import User

from Apps.user.view import user_bp, index
from extents import db, login, bootstrap
from flask_login import login_manager, current_user


# bootstrap = Bootstrap()


def create_app():
    #  Set templates path
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    #  import flask config file
    app.config.from_object(settings.DevConfig)
    #  blueprint
    app.register_blueprint(user_bp)  # Create a blueprint and bond the blueprint object
    app.register_blueprint(article_bp)  # Create a blueprint and bond the blueprint object
    bootstrap.init_app(app)
    db.init_app(app=app)
    login.init_app(app)
    login_manager.login_view = 'user/login'
    login.login_message_category = 'info'
    # register_template_context(app)
    print(app.url_map)
    return app


def register_template_context(app):
    @app.context_processor
    def make_template_context():
        if current_user.is_authenticated:
            admin = User.query.first()
            # categories = ArticleType.query.order_by(Category.name).all()
            return dict(admin=admin)
        else:
            pass
