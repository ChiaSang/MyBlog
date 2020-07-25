# -*- coding: utf-8 -*-
import random
from datetime import datetime

from faker import Faker

from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash

from Apps import User
from Apps.article.model import ArticleType, Article, Comment
from extents import db

fake = Faker()


def fake_admin():
    admin = User(
        name='admin',
        email=fake.email(),
        passwd=generate_password_hash('adminadmin'),
        blog_name=fake.sentence(),
        blog_sub_name=fake.sentence(),
    )
    db.session.add(admin)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()


def fake_categories(count=10):
    for i in range(count):
        category = ArticleType(type_name=fake.word())
        db.session.add(category)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def fake_posts(count=50):
    for i in range(count):
        post = Article(
            title=fake.sentence(),
            content=fake.text(2000),
            type_id=random.randint(1, ArticleType.query.count()),
            love_num=random.randint(1, ArticleType.query.count()),
            click_num=random.randint(1, 100),
            timestamp=datetime.now()
        )
        db.session.add(post)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()


def fake_comments(count=500):
    for i in range(count):
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            comment=fake.sentence(),
            timestamp=datetime.now(),
            love_num=random.randint(1, ArticleType.query.count()),
            reviewed=True,
            article_id=random.randint(1, Article.query.count())
        )
        db.session.add(comment)

    salt = int(count * 0.1)
    for i in range(salt):
        # unreviewed comments
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            comment=fake.sentence(),
            timestamp=datetime.now(),
            love_num=random.randint(1, ArticleType.query.count()),
            reviewed=False,
            article_id=random.randint(1, Article.query.count())
        )
        db.session.add(comment)

        # from admin
        comment = Comment(
            author='ChiaSang Victor',
            email='mima@example.com',
            comment=fake.sentence(),
            timestamp=datetime.now(),
            love_num=random.randint(1, ArticleType.query.count()),
            from_admin=True,
            reviewed=True,
            article_id=random.randint(1, Article.query.count())
        )
        db.session.add(comment)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()

    # replies
    for i in range(salt):
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            comment=fake.sentence(),
            love_num=random.randint(1, ArticleType.query.count()),
            timestamp=datetime.now(),
            reviewed=True,
            replied_id=random.randint(1, Comment.query.count()),
            article_id=random.randint(1, Article.query.count())
        )
        db.session.add(comment)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
