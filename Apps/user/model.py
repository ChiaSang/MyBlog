from datetime import datetime

from flask_login import UserMixin

from extents import db, login


@login.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32), nullable=False)
    passwd = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(64))
    phone = db.Column(db.String(16), unique=True, nullable=False)
    photo = db.Column(db.String(128))
    rtime = db.Column(db.DateTime, default=datetime.now)

    # articles = db.relationship('Article', backref='user')  # L2

    def get_id(self):
        return self.id

    def is_active(self):  # line 37
        return True

    def is_anonymous(self):
        return False

    # Required for administrative interface
    def __unicode__(self):
        return self.username
