# class User:
#     """
#     #  Define a User class
#     """
#     def __init__(self, username, passwd):
#         self.username = username
#         self.passwd = passwd
#
#     def __str__(self):
#         return self.username
from datetime import datetime

from extents import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32), nullable=False)
    passwd = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(64))
    phone = db.Column(db.String(16), unique=True, nullable=False)
    photo = db.Column(db.String(128))
    rtime = db.Column(db.DateTime, default=datetime.now)

    articles = db.relationship('Article', backref='user')
