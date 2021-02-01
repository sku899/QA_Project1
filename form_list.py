from wtforms import StringField, SubmitField, PasswordField, SelectField, validators
from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateField

class LoginForm(FlaskForm):
    email = StringField('email',validators=[validators.Email(granular_message=True)])
    password = PasswordField('password')
    signin = SubmitField('Sign In')
    test = SubmitField('test')
    entrydate =DateField()