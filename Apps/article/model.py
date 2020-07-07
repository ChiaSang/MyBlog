from datetime import datetime

from extents import db


class ArticleType(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type_name = db.Column(db.String(16), nullable=False)

    articles = db.relationship('Article', backref='article_type')
    #  这里注意驼峰法命名的表对象在引用的时候要使用下划线如⬆️


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    click_num = db.Column(db.Integer, default=0)
    love_num = db.Column(db.Integer, default=0)
    uid = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('article_type.id'), nullable=False)

    comments = db.relationship('Comment', backref='article')  # 通过文章找评论


class Comment(db.Model):
    # __tablename__ = 'table name'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comment = db.Column(db.String(255), nullable=False)
    uid = db.Column(db.Integer, db.ForeignKey('user.id'))
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))
    create_time = db.Column(db.DateTime, default=datetime.now)

    def __str__(self):
        return self.comment
