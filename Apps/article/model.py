from datetime import datetime

import bleach
from markdown import markdown

from extents import db


class ArticleType(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type_name = db.Column(db.String(16), nullable=False)

    articles = db.relationship('Article', backref='article_type')  # L1
    #  这里注意驼峰法命名的表对象在引用的时候要使用下划线如⬆️


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(64), nullable=False)
    content = db.Column(db.Text)
    content_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.now, index=True)
    click_num = db.Column(db.Integer, default=0)
    love_num = db.Column(db.Integer, default=0)
    # uid = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # L2
    type_id = db.Column(db.Integer, db.ForeignKey('article_type.id', ondelete='CASCADE'), nullable=False)  # L1

    # type = db.relationship('ArticleType', backref='article')
    # type = db.relationship('Article', backref='article_type')
    comments = db.relationship('Comment', backref='article', cascade='all, delete-orphan')  # 通过文章找评论 L3

    @staticmethod
    def on_changed_content(target, value, oldvalue, initiator):
        # allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
        #                 'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
        #                 'h1', 'h2', 'h3', 'p', 'img']
        # attrs = {
        #     '*': ['class'],
        #     'a': ['href', 'rel'],
        #     'img': ['src', 'alt'],
        # }
        # target.content_html = bleach.linkify(bleach.clean(
        #     markdown(value, output_format='html'),
        #     tags=allowed_tags, strip=True, attrs=attrs))
        target.content_html = markdown(value, output_format='html',
                                       extensions=['markdown.extensions.fenced_code', 'markdown.extensions.codehilite',
                                                   'markdown.extensions.tables', 'markdown.extensions.sane_lists'])


db.event.listen(Article.content, 'set', Article.on_changed_content)


class Comment(db.Model):
    # __tablename__ = 'table name'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author = db.Column(db.String(30))
    email = db.Column(db.String(254))
    comment = db.Column(db.Text, nullable=False)
    love_num = db.Column(db.Integer, default=0)
    from_admin = db.Column(db.Boolean, default=False)
    reviewed = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.now)

    article_id = db.Column(db.Integer, db.ForeignKey('article.id', ondelete='CASCADE'))  # L3
    # ondelete='CASCADE' 进行级联删除，删除文章后评论也随之删除，下面代码同上

    replied_id = db.Column(db.Integer, db.ForeignKey('comment.id', ondelete='CASCADE'))  # L4 自身引用
    replies = db.relationship('Comment', back_populates='replied', cascade='all, delete-orphan')  # L4 自身引用
    replied = db.relationship('Comment', back_populates='replies', remote_side=[id])  # L4 自身引用

    def __str__(self):
        return self.comment
