import re

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from Apps.user.model import User


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=16)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=16)])
    confirm = PasswordField('rePassword', validators=[DataRequired(), EqualTo('password')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone',
                        validators=[DataRequired(), Length(min=11, max=11, message='Phone Number is equal to 11 bit')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(name=username.data).first()
        if user:
            raise ValidationError('Username already existed')

    def validate_phone(self, phone):
        if re.search(r'^1[35678]\d{9}$', phone.data).group():
            phone_num = User.query.filter_by(phone=phone.data).first()
            if phone_num:
                raise ValidationError('Phone Number Error')
