from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, flash, session, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, validators
from wtforms.fields.html5 import DateField
import datetime
# from wtforms import DataRequired, ValidationError,Email, Length

app = Flask(__name__)
app.config['SECRET_KEY'] = 'YOUR_SECRET_KEY'
username='me'
password = 'qwerty123'
localhost = 'localhost:3306'
database = 'flaskdb'

app.config["SQLALCHEMY_DATABASE_URI"] = f'mysql+pymysql://{username}:{password}@{localhost}/{database}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app)



####table class
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

class Customers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(60), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    telephone = db.Column(db.String(12), nullable=False)
    gender = db.Column(db.String(2), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    booking = db.relationship('Bookings', backref='customers')

class Countries(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    countryname = db.Column(db.String(30), nullable=False)
    travel_vaccine = db.relationship('CVList', backref='countries')
    booking = db.relationship('Bookings', backref='countries')

class Vaccine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vaccinename = db.Column(db.String(30), nullable=False)
    travel_vaccine = db.relationship('CVList', backref='vaccine')
    booking = db.relationship('Bookings', backref='vaccine')

class CVList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    country_id = db.Column(db.Integer, db.ForeignKey('countries.id'), nullable=False)
    vaccine_id = db.Column(db.Integer, db.ForeignKey('vaccine.id'), nullable=False)

class Bookings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    weekday = db.Column(db.String(10), nullable=False)
    timeslot = db.Column(db.String(10), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey('countries.id'), nullable=False)
    vaccine_id = db.Column(db.Integer, db.ForeignKey('vaccine.id'), nullable=False)
    

###form setup
class LoginForm(FlaskForm):
    email = StringField('email',validators=[validators.Email(granular_message=True)])
    password = PasswordField('password')
    submit = SubmitField('Sign In')
    test = SubmitField('test')
    entrydate =DateField()

class SignUpForm(FlaskForm):
    firstname = StringField('First Name',validators=[validators.DataRequired()])
    lastname = StringField('Last Name',validators=[validators.DataRequired()])
    email = StringField('email',validators=[validators.Email(granular_message=True)])
    password = PasswordField('Password', validators=[validators.EqualTo('reenterpassword',message = "Password doesn't match")])
    reenterpassword = PasswordField('Re-Type Password', validators=[validators.Length(min=6,max=25)])
    telephone = StringField('Telephone',validators=[validators.DataRequired()])
    gender = SelectField('Gender',choices=['M','F'])
    age = StringField('Age',validators=[validators.DataRequired()])
    submit = SubmitField('Sign Up')

class UpdateForm(FlaskForm):
    firstname = StringField('First Name',validators=[validators.DataRequired()])
    lastname = StringField('Last Name',validators=[validators.DataRequired()])
    email = StringField('email',validators=[validators.Email(granular_message=True)])
    telephone = StringField('Telephone',validators=[validators.DataRequired()])
    gender = SelectField('Gender',choices=['M','F'])
    age = StringField('Age',validators=[validators.DataRequired()])
    update = SubmitField('Update')
    delete = SubmitField('Delete')

class BookingForm(FlaskForm):
    country = SelectField('Travel Country',choices=[])
    vaccine = SelectField('Vaccine',choices=[])
    submit = SubmitField('Book an Appointment')
    go = SubmitField('Go')
    entrydate =DateField('Date')#,validators=[validators.DataRequired()])
    timeslot = SelectField('Time Slot',choices=['9:30am','10:30am','11:30am','13:30pm','14:30pm','15:30pm'])

####Functions
def is_exist(customers, email):
    for customer in customers:
        if (email == customer.email):
            return True
    return False

def is_same_password(customers, password, email):
    for customer in customers:
        if (email == customer.email) and (password == customer.password):
            return True
    return False

def add_customer(frm):
    first_name = frm.firstname.data
    last_name = frm.lastname.data
    email = frm.email.data
    password = frm.password.data
    telephone = frm.telephone.data
    gender = frm.gender.data
    age = frm.age.data
    customer = Customers(first_name=first_name, last_name=last_name, email=email,\
        password = password, telephone=telephone, gender=gender, age=age)
    return customer


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def register():
    error = ""
    form = LoginForm()
    email = form.email.data
    password = form.password.data
    if form.test.data:
        session['initial']=True
        return redirect(url_for("booking"))
    if  not form.validate_on_submit():        
        if form.email.errors:
            email=""
        if form.password.errors:
            password=""
        form.email.data = email
        form.password.data = password
        return render_template('login.html', form = form)
    else:
        if is_exist(Customers.query.all(), form.email.data):
            if is_same_password(Customers.query.all(), form.password.data, form.email.data):
                # return render_template('login.html', form = form,message = "existing customer with correct password")
                session['count'] = 1
                session['email'] = email
                session['greeting'] = 'Welcome back'
                return redirect(url_for('update'))
            else:
                return render_template('login.html', form = form,message = "Password is incorrect. Please try again.")

        else: # new user
            session['email'] =  email
            session['password'] = password
            session['count'] = 1
            return redirect(url_for('signup'))
    #return render_template('signup.html', form = form, customer=)
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    a=1
    if a==1:
        form.gender.choices =['M','F','Perfer Not to Say']
    #currentpassword = form.password.data
    if session['count'] ==1:
        form.email.data = session.get('email')
        session['count'] = 2
    
    if  form.validate_on_submit(): ## everything is OK
        # if len(Customers.query.all()) ==0:
        #     return render_template('signup.html', form = form,message = 'New customer')
        # else:
        
        if is_exist(Customers.query.all(), form.email.data):
            return render_template('signup.html', form = form,message = 'Existing customer')
        else:
            customer = add_customer(form)
            #customer.password = currentpaessword
            db.session.add(customer)
            name = customer.first_name +" "+ customer.last_name
            db.session.commit()
            output_message = f"Hi {name}, your account has been added. Here is your details."
            session['greeting'] = 'Welcome to join'
            return render_template('update.html', form = form,message = output_message)
    else:
        return render_template('signup.html', form = form , message = 'Please check your data')
    #return render_template('signup.html', form = form)


@app.route('/update', methods=['GET', 'POST'])
def update():
    form = UpdateForm()
    currentemail = session['email']
    customer = Customers.query.filter_by(email=session['email']).first()
    if session['count'] == 1:
        form.firstname.data = customer.first_name
        form.lastname.data = customer.last_name
        form.email.data = customer.email
        form.telephone.data = customer.telephone
        form.gender.data = customer.gender
        form.age.data = customer.age
        session['name']= customer.first_name +" "+customer.last_name
        session['count'] = 2
    if form.update.data and form.validate_on_submit(): ##update record
        customer.first_name =form.firstname.data
        form.lastname.data = customer.last_name
        customer.email = form.email.data
        customer.telephone = form.telephone.data
        customer.gender = form.gender.data
        customer.age = form.age.data
        db.session.commit()
        return render_template('update.html', form = form, message = 'Update record successfully.')
    if form.delete.data:
        db.session.delete(customer)
        db.session.commit()
        return f"Hi {session['name']}, your account has been deleted.<br/>"
    return render_template('update.html', form = form, customer = session['name'],greeting=session['greeting'])

@app.route('/booking', methods=['GET', 'POST'])
def booking():
    form = BookingForm()
    allcounties = Countries.query.all()
    country_list=[]
    for country in allcounties:
       country_list.append(country.countryname)
    form.country.choices =country_list
    if not session['initial']:
        selected_country = form.country.data
        country_id = Countries.query.filter_by(countryname = selected_country).first().id
        vaccine_list=[]
        selected_country_vaccine = CVList.query.filter_by(country_id = country_id).all()
        for v in selected_country_vaccine:
            vaccine_list.append(Vaccine.query.filter_by(id = v.vaccine_id).first().vaccinename)
        form.vaccine.choices=vaccine_list
    # self.cleaned_data['date'] 
    session['initial'] =False
    selected_date = form.entrydate.data
    is_date_right = True
    error = ""
    if not selected_date is None:
        is_date_right = is_date_right and selected_date > datetime.date.today() and selected_date.weekday()<5
        error = "Selected day must later than today between Monday to Friday."
    else:
        is_date_right =False
        error = "No date is selected. Selected day must later than today between Monday to Friday."
    is_vaccine_selected = True
    if form.vaccine.data is None:
        error += "<br> No vaccine is selected. Press 'Go' button to enable selection"
        is_vaccine_selected = False
    weekday =['Monday','Tuesday', 'Wednesday', 'Thursday','Friday']
    if form.submit.data and is_date_right and is_vaccine_selected:# and form.validate_on_submit():
        return f"A vaccine {form.vaccine.data} appointment has been booked on {weekday[selected_date.weekday()]}, {form.entrydate.data}, at {form.timeslot.data} for travelling to {form.country.data}"
    session['initial']=False

   
    return render_template('booking.html', form = form, message = error)
    

    #return render_template('update.html', form = form)
#     



if __name__ == '__main__':
     app.run(debug=True, host='0.0.0.0')