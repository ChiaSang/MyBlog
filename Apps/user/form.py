from typing import re

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=8)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=16)])
    confirm = PasswordField('rePassword', validators=[DataRequired(), EqualTo('password')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=11, max=11, message='Phone Number is equal to 11 bit')])
    submit = SubmitField('Register')


    def validate_phone(self, phone):
        phone = phone.data
        if not re.search(r'^1[35678]\d{9}$', phone):
            raise ValidationError('Phone Number Error')
