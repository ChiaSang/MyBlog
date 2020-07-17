import re

from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp

from Apps.user.model import User


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),
                                                   Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                          'Username must have only letters, numbers, dots or '
                                                          'underscores'), Length(min=4, max=16)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=16)])
    confirm = PasswordField('rePassword',
                            validators=[DataRequired(), EqualTo('password', message='Passwords must match.')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(name=username.data).first()
        if user:
            raise ValidationError('Username already existed')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('Email already registered.')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=16)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=16)])
    remember = BooleanField('Remember')
    submit = SubmitField('Login')


class EditProfileForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    username = StringField('Username', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Usernames must have only letters, numbers, dots or '
               'underscores')])
    blog_name = StringField('Blog Name', validators=[DataRequired(), Length(max=64)])
    blog_sub_name = StringField('Blog Sub Name', validators=[DataRequired(), Length(max=256)])
    submit = SubmitField('Submit')

    # def __init__(self, user, *args, **kwargs):
    #     super(EditProfileForm, self).__init__(*args, **kwargs)
    #     self.user = user

    # def validate_username(self, username):
    #     user = User.query.filter_by(name=username.data).first()
    #     if user:
    #         raise ValidationError('Username already existed')
    #
    # def validate_email(self, email):
    #     email = User.query.filter_by(email=email.data).first()
    #     if email:
    #         raise ValidationError('Email already registered.')
