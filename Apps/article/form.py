from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from Apps.user.model import User


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(1, 60)])
    category = SelectField('Category', coerce=int, default=1)
    body = StringField('Body', validators=[DataRequired()])
    submit = SubmitField()

    # def __init__(self, *args, **kwargs):
    #     super(PostForm, self).__init__(*args, **kwargs)
    #     self.category.choices = [(category.id, category.name)
    #                              for category in Category.query.order_by(Category.name).all()]
