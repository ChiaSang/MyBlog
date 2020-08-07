from flask import flash
from flask_pagedown.fields import PageDownField
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from Apps.article.model import ArticleType
from Apps.user.model import User


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(1, 60)])
    category = SelectField('Category', coerce=int, default=1)
    body = PageDownField('Body', validators=[DataRequired()])
    submit = SubmitField()

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.category.choices = [(category.id, category.type_name)
                                 for category in ArticleType.query.order_by(ArticleType.type_name).all()]


class CommentForm(FlaskForm):
    author = StringField('Name', validators=[DataRequired(), Length(1, 30)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(1, 254)])
    body = TextAreaField('Comment', validators=[DataRequired()])
    recaptcha = RecaptchaField()
    submit = SubmitField()
