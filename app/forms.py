# app/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class FeedbackForm(FlaskForm):
    feedback = TextAreaField('Your Feedback', validators=[DataRequired(), Length(min=10, max=500)])
    category = SelectField(
        'Category',
        choices=[('Service', 'Service'), ('Cleanliness', 'Cleanliness'), ('Staff', 'Staff'), ('Other', 'Other')],
        validators=[DataRequired()]
    )
    submit = SubmitField('Submit Feedback')
