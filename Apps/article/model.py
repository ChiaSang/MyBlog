from datetime import datetime

from extents import db


class ArticleType(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type_name = db.Column(db.String(16), nullable=False)

    articles = db.relationship('Article', backref='article_type')  # L1
    #  这里注意驼峰法命名的表对象在引用的时候要使用下划线如⬆️


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    click_num = db.Column(db.Integer, default=0)
    love_num = db.Column(db.Integer, default=0)
    # uid = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # L2
    type_id = db.Column(db.Integer, db.ForeignKey('article_type.id'), nullable=False)  # L1

    # type = db.relationship('ArticleType', backref='article')
    # type = db.relationship('Article', backref='article_type')
    comments = db.relationship('Comment', backref='article', cascade='all, delete-orphan')  # 通过文章找评论 L3


class Comment(db.Model):
    # __tablename__ = 'table name'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author = db.Column(db.String(30))
    email = db.Column(db.String(254))
    comment = db.Column(db.Text, nullable=False)
    love_num = db.Column(db.Integer, default=0)
    from_admin = db.Column(db.Boolean, default=False)
    reviewed = db.Column(db.Boolean, default=False)
    create_time = db.Column(db.DateTime, default=datetime.now)

    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))  # L3

    replied_id = db.Column(db.Integer, db.ForeignKey('comment.id'))  # L4 自身引用
    replies = db.relationship('Comment', back_populates='replied', cascade='all, delete-orphan')  # L4 自身引用
    replied = db.relationship('Comment', back_populates='replies', remote_side=[id])  # L4 自身引用

    def __str__(self):
        return self.comment
