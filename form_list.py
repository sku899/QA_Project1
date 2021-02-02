from wtforms import StringField, SubmitField, PasswordField, SelectField, validators
from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateField

class LoginForm(FlaskForm):
    email = StringField('User email',validators=[validators.Email(granular_message=True)])
    password = PasswordField('Password')
    login = SubmitField('Login')
    register = SubmitField('Create New Account')
    #entrydate =DateField()