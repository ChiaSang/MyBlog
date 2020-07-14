from flask import Flask

from settings import config
from Apps.article.view import article_bp
from Apps.user.model import User

from Apps.user.view import user_bp, index
from extents import db, bootstrap, login
from flask_login import login_manager


def create_app(config_name):
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    app.register_blueprint(user_bp)  # Create a blueprint and bond the blueprint object
    app.register_blueprint(article_bp)  # Create a blueprint and bond the blueprint object
    bootstrap.init_app(app)
    db.init_app(app)
    login.init_app(app)
    login_manager.login_view = 'user.user_login'
    login.login_message_category = 'info'
    # register_template_context(app)
    # print(app.url_map)
    return app

# def register_template_context(app):
#     @app.context_processor
#     def make_template_context():
#         if current_user.is_authenticated:
#             admin = User.query.first()
#             # categories = ArticleType.query.order_by(Category.name).all()
#             return dict(admin=admin)
#         else:
#             pass
