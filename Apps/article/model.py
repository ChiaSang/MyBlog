from datetime import datetime

from extents import db


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    click_num = db.Column(db.Integer, default=0)
    love_num = db.Column(db.Integer, default=0)
    uid = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)