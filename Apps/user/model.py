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
    name = db.Column(db.String(20), nullable=False)
    passwd = db.Column(db.String(20), nullable=False)
    repass = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(20), unique=True)
    rtime = db.Column(db.DateTime, default=datetime.now)

    def __str__(self):
        return self.name
