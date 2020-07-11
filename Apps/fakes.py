# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li <withlihui@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
import random

from faker import Faker
from sqlalchemy.exc import IntegrityError

from Apps.article.model import ArticleType, Article, Comment
from extents import db

fake = Faker()


def fake_me():
    def fake_categories(count=10):
        category = ArticleType(name='Default')
        db.session.add(category)

        for i in range(count):
            category = ArticleType(name=fake.word())
            db.session.add(category)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    def fake_posts(count=50):
        for i in range(count):
            post = Article(
                title=fake.sentence(),
                body=fake.text(2000),
                category=ArticleType.query.get(random.randint(1, ArticleType.query.count())),
                timestamp=fake.date_time_this_year()
            )

            db.session.add(post)
        db.session.commit()

    def fake_comments(count=500):
        for i in range(count):
            comment = Comment(
                author=fake.name(),
                email=fake.email(),
                site=fake.url(),
                body=fake.sentence(),
                timestamp=fake.date_time_this_year(),
                reviewed=True,
                post=Article.query.get(random.randint(1, Article.query.count()))
            )
            db.session.add(comment)

        salt = int(count * 0.1)
        for i in range(salt):
            # unreviewed comments
            comment = Comment(
                author=fake.name(),
                email=fake.email(),
                site=fake.url(),
                body=fake.sentence(),
                timestamp=fake.date_time_this_year(),
                reviewed=False,
                post=Article.query.get(random.randint(1, Article.query.count()))
            )
            db.session.add(comment)

            # from admin
            comment = Comment(
                author='Mima Kirigoe',
                email='mima@example.com',
                site='example.com',
                body=fake.sentence(),
                timestamp=fake.date_time_this_year(),
                from_admin=True,
                reviewed=True,
                post=Article.query.get(random.randint(1, Article.query.count()))
            )
            db.session.add(comment)
        db.session.commit()

        # replies
        for i in range(salt):
            comment = Comment(
                author=fake.name(),
                email=fake.email(),
                site=fake.url(),
                body=fake.sentence(),
                timestamp=fake.date_time_this_year(),
                reviewed=True,
                replied=Comment.query.get(random.randint(1, Comment.query.count())),
                post=Article.query.get(random.randint(1, Article.query.count()))
            )
            db.session.add(comment)
        db.session.commit()


fakeme = fake_me()
