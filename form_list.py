from wtforms import StringField, SubmitField, PasswordField, SelectField, validators
from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateField

class LoginForm(FlaskForm):
    email = StringField('User email',validators=[validators.Email(granular_message=True)])
    password = PasswordField('Password')
    login = SubmitField('Login')
    register = SubmitField('Create New Account')
    #entrydate =DateField()
    

class SignUpForm(FlaskForm):
    firstname = StringField('First Name',validators=[validators.DataRequired()])
    lastname = StringField('Last Name',validators=[validators.DataRequired()])
    email = StringField('email',validators=[validators.Email(granular_message=True)])
    password = PasswordField('Password', validators=[validators.Length(min=6,max=25,message="Password  must be between 6 and 25 characters long"),
     validators.EqualTo('reenterpassword',message = "Password doesn't match")])
    reenterpassword = PasswordField('Re-Type Password')
    telephone = StringField('Telephone',validators=[validators.DataRequired()])
    gender = SelectField('Gender',choices=['M','F'])
    age = StringField('Age',validators=[validators.DataRequired()])
    submit = SubmitField('Create New Account')

class UpdateForm(FlaskForm):
    firstname = StringField('First Name',validators=[validators.DataRequired()])
    lastname = StringField('Last Name',validators=[validators.DataRequired()])
    email = StringField('email',validators=[validators.Email(granular_message=True)])
    telephone = StringField('Telephone',validators=[validators.DataRequired()])
    gender = SelectField('Gender',choices=['M','F'])
    age = StringField('Age',validators=[validators.DataRequired()])
    update = SubmitField('Update your Account')
    delete = SubmitField('Delete your Account')
    booking = SubmitField('Create an Appointment')

class BookingForm(FlaskForm):
    country = SelectField('Travel Country',choices=[])
    vaccine = SelectField('Vaccine',choices=[])
    create = SubmitField('Create an Appointment')
    go = SubmitField('Retrieve Vaccine')
    entrydate =DateField('Date')#,validators=[validators.DataRequired()])
    timeslot = SelectField('Time Slot',choices=['9:30am','10:30am','11:30am','13:30pm','14:30pm','15:30pm'])
    delete=  SubmitField('Delete selected Appointment')
    update=  SubmitField('Update selected Appointment')
    appointments =SelectField('Appointments',choices=[])
    back=  SubmitField('Back to Manual')


class ActionsForm(FlaskForm):
    update = SubmitField('Update Your Account')
    booking =SubmitField('Manage Your Appointments')
    logout =SubmitField('Log out')

class UpdateBookingForm(FlaskForm):
    country = SelectField('Travel Country',choices=[])
    vaccine = SelectField('Vaccine',choices=[])
    submit = SubmitField('Create an Appointment')
    go = SubmitField('Retrieve Vaccine')
    entrydate =DateField('Date')#,validators=[validators.DataRequired()])
    timeslot = SelectField('Time Slot',choices=['9:30am','10:30am','11:30am','13:30pm','14:30pm','15:30pm'])
    update=  SubmitField('Update this Appointment')
    cancel = SubmitField('Cancel')