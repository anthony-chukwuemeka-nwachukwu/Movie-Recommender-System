from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, HiddenField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from src import db
from src.models.user import User
from src.param import min_required_no_of_movies_by_user


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=15)])
    password_confirm = PasswordField('Confirm Password',
                                     validators=[DataRequired(), Length(min=6, max=15), EqualTo('password')])
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=55)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=55)])
    stared_valid = HiddenField(default='not-validated', id="stared_valid")
    stared_ids = HiddenField(default='not-validated', id="stared_ids")
    submit = SubmitField('Register Now')

    def validate_email(self, email):
        user = db.session.query(User).filter(User.username == email.data).first() is not None
        if user:
            raise ValidationError('Email is already in use. Login instead')

    def validate_stared(self, stared_valid):
        if str(stared_valid.data) == 'not-validated':
            raise ValidationError('Click on Validation to validate')
        if str(stared_valid.data) != 'true':
            raise ValidationError('Select a minimum of {} movies in all genres'.format(min_required_no_of_movies_by_user))
