import click
from flask import Flask, app

from settings import config
from Apps.article.view import article_bp
from Apps.user.model import User

from Apps.user.view import user_bp, index
from extents import db, bootstrap, login, pagedown
from flask_login import login_manager


def create_app(config_name):
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    app.register_blueprint(user_bp)  # Create a blueprint and bond the blueprint object
    app.register_blueprint(article_bp)  # Create a blueprint and bond the blueprint object
    bootstrap.init_app(app)
    db.init_app(app)
    pagedown.init_app(app)
    login.init_app(app)
    login_manager.login_view = 'user.user_login'
    login.login_message_category = 'info'
    register_commands(app)
    # print(app.url_map)
    return app


def register_commands(app):
    @app.cli.command()
    @click.option('--category', default=10, help='Quantity of categories, default is 10.')
    @click.option('--post', default=50, help='Quantity of posts, default is 50.')
    @click.option('--comment', default=500, help='Quantity of comments, default is 500.')
    def forge(category, post, comment):
        """Generate fake data."""
        from fakes import fake_admin, fake_categories, fake_comments, fake_posts

        db.drop_all()
        db.create_all()

        click.echo('Generating the administrator...')
        fake_admin()

        click.echo('Generating %d categories...' % category)
        fake_categories(category)

        click.echo('Generating %d posts...' % post)
        fake_posts(post)

        click.echo('Generating %d comments...' % comment)
        fake_comments(comment)

        click.echo('Done.')