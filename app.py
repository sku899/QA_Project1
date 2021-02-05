from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, flash, session, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, validators
from wtforms.fields.html5 import DateField
import datetime
# from wtforms import DataRequired, ValidationError,Email, Length
import form_list as frm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'YOUR_SECRET_KEY'
username='me'
password = 'qwerty123'
ocalhost = 'localhost:3306'
database = 'flaskdb'

#app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{username}:{password}@{localhost}/{database}"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://me:qwerty123@localhost:3306/flaskdb"
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
# class LoginForm(FlaskForm):
#     email = StringField('email',validators=[validators.Email(granular_message=True)])
#     password = PasswordField('password')
#     signin = SubmitField('Sign In')
#     test = SubmitField('test')
#     entrydate =DateField()

# class SignUpForm(FlaskForm):
#     firstname = StringField('First Name',validators=[validators.DataRequired()])
#     lastname = StringField('Last Name',validators=[validators.DataRequired()])
#     email = StringField('email',validators=[validators.Email(granular_message=True)])
#     password = PasswordField('Password', validators=[validators.Length(min=6,max=25), validators.EqualTo('reenterpassword',message = "Password doesn't match")])
#     reenterpassword = PasswordField('Re-Type Password', validators=[validators.Length(min=6,max=25)])
#     telephone = StringField('Telephone',validators=[validators.DataRequired()])
#     gender = SelectField('Gender',choices=['M','F'])
#     age = StringField('Age',validators=[validators.DataRequired()])
#     submit = SubmitField('Create New Account')

# class UpdateForm(FlaskForm):
#     firstname = StringField('First Name',validators=[validators.DataRequired()])
#     lastname = StringField('Last Name',validators=[validators.DataRequired()])
#     email = StringField('email',validators=[validators.Email(granular_message=True)])
#     telephone = StringField('Telephone',validators=[validators.DataRequired()])
#     gender = SelectField('Gender',choices=['M','F'])
#     age = StringField('Age',validators=[validators.DataRequired()])
#     update = SubmitField('Update your Account')
#     delete = SubmitField('Delete your Account')
#     booking = SubmitField('Create an Appointment')

# class BookingForm(FlaskForm):
#     country = SelectField('Travel Country',choices=[])
#     vaccine = SelectField('Vaccine',choices=[])
#     submit = SubmitField('Create an Appointment')
#     go = SubmitField('Retrieve Vaccine')
#     entrydate =DateField('Date')#,validators=[validators.DataRequired()])
#     timeslot = SelectField('Time Slot',choices=['9:30am','10:30am','11:30am','13:30pm','14:30pm','15:30pm'])
#     delete=  SubmitField('Delete selected Appointment')
#     update=  SubmitField('Update selected Appointment')
#     appointments =SelectField('Appointments',choices=[])
#     back=  SubmitField('Back to Manual')

# class ActionsForm(FlaskForm):
#     update = SubmitField('Update Your Account')
#     booking =SubmitField('Manage Your Appointments')
#     logout =SubmitField('Log out')

# class UpdateBookingForm(FlaskForm):
#     country = SelectField('Travel Country',choices=[])
#     vaccine = SelectField('Vaccine',choices=[])
#     submit = SubmitField('Create an Appointment')
#     go = SubmitField('Retrieve Vaccine')
#     entrydate =DateField('Date')#,validators=[validators.DataRequired()])
#     timeslot = SelectField('Time Slot',choices=['9:30am','10:30am','11:30am','13:30pm','14:30pm','15:30pm'])
#     update=  SubmitField('Update this Appointment')
#     cancel = SubmitField('Cancel')

####Functions
def is_exist(customers, email):
    for customer in customers:
        if (email == customer.email):
            return True
    return False

def is_same_password(customers, password, email):
    for customer in customers:
        if (email.lower() == customer.email.lower()) and (password == customer.password):
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


def get_appointment_list(appointments):
    if len(appointments) ==0:
        app_list =["You don't have any appointment yet."]
    else:
        app_list=[f"You have the following {len(appointments)} appointment(s)", 'Date       ' + 'Weekday     '+'Time Solt      '+'Country      '+'Vaccine     ']
        for appointment in appointments:
            countryname = Countries.query.filter_by(id = appointment.country_id).first().countryname
            vaccinename = Vaccine.query.filter_by(id = appointment.vaccine_id).first().vaccinename
            tbl_string = str(appointment.date.date().strftime('%d-%b-%Y'))+" "+\
                appointment.weekday+" " + appointment.timeslot+" "+\
                appointment.countries.countryname+" "+appointment.vaccine.vaccinename
            app_list.append(tbl_string)
    return app_list


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def login():
    error = ""
    form = frm.LoginForm()
    email = form.email.data
    password = form.password.data
    # if session['email']=='':
    #     pass
    if form.register.data:
        session['initial']=True
        return redirect(url_for("signup"))
    if  not form.validate_on_submit():        
        if form.email.errors:
            email=""
        if form.password.errors:
            password=""
        form.email.data = email
        # if len(session['email']) >0 :
        #     form.email.data=session['mail']
        form.password.data = password
        return render_template('login.html', form = form)
    else:
        if is_exist(Customers.query.all(), form.email.data): ## return customer
            ##login successfully
            if is_same_password(Customers.query.all(), form.password.data, form.email.data):
                # return render_template('login.html', form = form,message = "existing customer with correct password")
                session['count'] = 1
                session['email'] = email
                session['greeting'] = 'Welcome back'
                return redirect(url_for('actions'))
            else:
                form.email.data = email=""
                return render_template('login.html', form = form, message = "**Password is incorrect. Please try again." )
        else: # new user
            session['email'] =  email
            session['password'] = password
            session['count'] = 1
            form.email.data = email
            return render_template('login.html', form = form, message = "**New User?? Please Register." )
    #return render_template('signup.html', form = form, customer=)
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = frm.SignUpForm()
    errmsg=""
    #currentpassword = form.password.data
    if session['count'] ==1:
        form.email.data = session.get('email')
        session['count'] = 2
    
    if  form.validate_on_submit(): ## everything is OK
        # if len(Customers.query.all()) ==0:
        #     return render_template('signup.html', form = form,message = 'New customer')
        # else:
        email =  form.email.data
        if is_exist(Customers.query.all(), form.email.data):
            #return render_template('signup.html', form = form,message = 'Existing customer')
            session['mail'] = email
            return redirect(url_for('login'))
        else:
            customer = add_customer(form)
            #customer.password = currentpaessword
            db.session.add(customer)
            name = form.firstname.data +" " +form.lastname.data #customer.first_name +" "+ customer.last_name
            db.session.commit()
            output_message = f"Hi {name}, your account has been added. Here is your details."
            session['greeting'] = 'Welcome to join'
            session['email'] = email
            session['count'] = 1
            return redirect(url_for('update'))
            #return render_template('update.html', form = form,message = output_message)
    else:
        errmsg = 'Please check your data. All fields are required'
    return render_template('signup.html', form = form , message = errmsg)
    #return render_template('signup.html', form = form)


@app.route('/update', methods=['GET', 'POST'])
def update():
    form = frm.UpdateForm()
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
        session['id'] = Customers.query.filter_by(email = session['email']).first().id
    if form.update.data and form.validate_on_submit(): ##update record
        customer.first_name =form.firstname.data
        form.lastname.data = customer.last_name
        customer.email = form.email.data
        customer.telephone = form.telephone.data
        customer.gender = form.gender.data
        customer.age = form.age.data
        db.session.commit()
        session['name'] = form.firstname.data +" "+ customer.last_name
        session['greeting'] ="Account updated"
        return render_template('update.html', form = form, customer = session['name'],greeting=session['greeting'],message = 'Update record successfully.')
    if form.delete.data:
        num_of_apps = len(Bookings.query.filter_by(customer_id=customer.id).all())
        if num_of_apps ==0:
            db.session.delete(customer)
            db.session.commit()
            return f"Hi {session['name']}, your account has been deleted.<br/>"
        else:
            return render_template('update.html', form = form, customer = session['name'],greeting=session['greeting'],message = f'You have {num_of_apps} account(s) with us. You cannot withdraw the account now.')
    if form.booking.data:
        session['initial']=True
        session['from'] = ''
        return redirect(url_for('booking'))
    return render_template('update.html', form = form, customer = session['name'],greeting=session['greeting'])

@app.route('/booking', methods=['GET', 'POST'])
def booking():
    form = frm.BookingForm()
    customer = Customers.query.filter_by(id = session['id']).first()
    msg=''
    if session['from'] == 'update':
        msg = session['original_app'] + " has been changed to " + session['updated_app']+"."
        if session['updated_app']=='':
            msg = session['original_app'] + " is not changed. "
        session['from']=''
    ##update appointments list  
    # appointments = Bookings.query.filter_by(customer_id=customer.id).all()
    # app_list=['Date' + 'Weekday     '+'Time Solt      '+'Country      '+'Vaccine     ']
    # for appointment in appointments:
    #     countryname = Countries.query.filter_by(id = appointment.country_id).first().countryname
    #     vaccinename = Vaccine.query.filter_by(id = appointment.vaccine_id).first().vaccinename
    #     tbl_string = str(appointment.date.date().strftime('%d-%b-%Y')) + " "+appointment.weekday + " "+appointment.timeslot+\
    #         " "+countryname.center(12)+" "+vaccinename.center(20)
    #     app_list.append(tbl_string)
    # form.appointments.choices =  app_list
    appointments = Bookings.query.filter_by(customer_id=customer.id).all()
    app_list = get_appointment_list(appointments)
    form.appointments.choices = app_list[0:1] +app_list[2:]
    
    allcounties = Countries.query.all()
    country_list=[]
    for country in allcounties:
        country_list.append(country.__dict__["countryname"])
    #    country_list.append(country.countryname)
    form.country.choices =country_list
    if session['initial']:
        selected_country = country_list[0]
        form.entrydate.data= datetime.date.today()
        session['initial'] =False
    else:
        selected_country = form.country.data
    country_id = Countries.query.filter_by(countryname = selected_country).first().id
    vaccine_list=[]
    selected_country_vaccine = CVList.query.filter_by(country_id = country_id).all()
    for v in selected_country_vaccine:
        vaccine_list.append(Vaccine.query.filter_by(id = v.vaccine_id).first().vaccinename)
    form.vaccine.choices=vaccine_list
    # self.cleaned_data['date'] 
    
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
    
    if form.submit.data:
        if is_date_right and is_vaccine_selected:# and form.validate_on_submit():
            customer = Customers.query.filter_by(id = session['id']).first()
            name = customer.first_name +" "+customer.last_name##
            ###
            date = selected_date
            weekday = weekday[selected_date.weekday()]
            timeslot = form.timeslot.data
            customer_id = session['id']
            country_id = Countries.query.filter_by(countryname=form.country.data).first().id
            vaccine_id = Vaccine.query.filter_by(vaccinename=form.vaccine.data).first().id 
            booking_to_add = Bookings(date=date, weekday=weekday, timeslot = timeslot,customer_id=customer_id, country_id= country_id, vaccine_id=vaccine_id)
            db.session.add(booking_to_add)
            db.session.commit()
            
            app_list.append(str(selected_date.strftime('%d-%b-%Y')).center(12) + " "+weekday.center(10) + timeslot.center(10)+\
                form.country.data.center(12)+form.vaccine.data.center(20))
            appointments = Bookings.query.filter_by(customer_id=customer.id).all()
            app_list = get_appointment_list(appointments)
            form.appointments.choices = app_list[0:1] +app_list[2:]
            return render_template('booking.html', form = form, message = app_list,msg = app_list[-1] + " has been added." )
        else:
            errmsg ="**error: "
            if not is_date_right:
                errmsg += "Selected date must be a working day later than today. "
            if not is_vaccine_selected:
                errmsg += "Make sure vaccine is selected."

            return render_template('booking.html', form = form, message = app_list,msg = errmsg )
        #return f"Hi, {name}, a vaccine {form.vaccine.data} appointment has been booked on {weekday[selected_date.weekday()]}, {form.entrydate.data}, at {form.timeslot.data} for travelling to {form.country.data}"
    if form.delete.data or form.update.data:
        if not (form.appointments.data[0:3].upper()=='YOU'):
            customer_id = customer.id
            delete_appointment= form.appointments.data
            raw_columns = delete_appointment.split(' ')
            columns=[]
            for rc in raw_columns:
                if len(rc.strip())>0:
                    columns.append(rc.strip())
            date= datetime.datetime.strptime(columns[0]+ " 00:00:00", '%d-%b-%Y %H:%M:%S')
            columns[0]=date
            weekday = columns[1]
            timeslot = columns[2]
            #customer_id = session['id']
            country_id = Countries.query.filter_by(countryname=columns[3]).first().id
            vaccine_id = Vaccine.query.filter_by(vaccinename=columns[4]).first().id 
            columns[3]=customer_id
            columns[4]=country_id
            columns.append(vaccine_id)
            appointments_to_delete = Bookings.query.filter_by(date=date, weekday=weekday, timeslot = timeslot,customer_id=customer_id, country_id= country_id, vaccine_id=vaccine_id).first()
            if form.delete.data:
                db.session.delete(appointments_to_delete)
                db.session.commit()
                app_list.remove(delete_appointment)
                appointments = Bookings.query.filter_by(customer_id=customer.id).all()
                app_list = get_appointment_list(appointments)
                form.appointments.choices = app_list[0:1] +app_list[2:]
                return render_template('booking.html', form = form, message = app_list ,msg = delete_appointment + " has been deleted.")
            else:
                session['appointment']=columns
                session['initial']=True
                session['id']=customer.id
                session['app_to_update']=form.appointments.data
                return redirect(url_for('updatebooking'))
        else:
            return render_template('booking.html', form = form, message=app_list, msg='**error: No appointment is selected.')
    if form.back.data:
        session['count'] = 1
        session['email'] = customer.email
        session['greeting'] = 'Welcome back'
        return redirect(url_for('actions'))
    session['initial']=False   
    return render_template('booking.html', form = form, message=app_list, msg=msg)  
    #return render_template('update.html', form = form)
#     



@app.route('/actions', methods=['GET', 'POST'])
def actions():
    form = frm.ActionsForm()
    email = session['email']
    customer = Customers.query.filter_by(email = email).first()
    title = f"{session['greeting']}, {customer.first_name+' '+customer.last_name}, you can view your account details and book an appointment."
    appointments = Bookings.query.filter_by(customer_id=customer.id).all()
    appointment_list = get_appointment_list(appointments)
    if form.booking.data:
        session['id']=customer.id
        session['initial']=True
        session['from']='action'
        return redirect(url_for('booking'))
    if form.update.data:
        session['greeting'] = 'Welcome back'
        session['email'] = email
        session['count'] = 1
        return redirect(url_for('update'))
    if form.logout.data:
        session['count'] = 0
        session['email'] = ''
        session['greeting'] = ''
        return redirect(url_for('login'))
        

    return render_template('actions.html', form = form, title=title, message=appointment_list)  


@app.route('/updatebooking', methods=['GET', 'POST'])
def updatebooking():
    form=frm.UpdateBookingForm()
    col =session['appointment']
    appointment=Bookings.query.filter_by(date=col[0].isoformat(), weekday=col[1], timeslot = col[2],customer_id=col[3], country_id= col[4], vaccine_id=col[5]).first()
    if session['initial']:
        allcounties = Countries.query.all()
        country_list=[]
        for country in allcounties:
            country_list.append(country.countryname)
        form.country.choices =country_list
        col =session['appointment']
        vaccine_list=[]
        selected_country_vaccine = CVList.query.filter_by(country_id = col[4]).all()
        for v in selected_country_vaccine:
            vaccine_list.append(Vaccine.query.filter_by(id = v.vaccine_id).first().vaccinename)

        form.vaccine.choices=vaccine_list
        countryname = Countries.query.filter_by(id = col[4]).first().countryname
        form.country.data= countryname
        vaccinename = Vaccine.query.filter_by(id = col[5]).first().vaccinename
        form.vaccine.data=vaccinename
        
        form.entrydate.data = appointment.date
        form.timeslot.data=appointment.timeslot 
        session['initial']=False
    
    ###
    is_date_right = True
    selected_date = form.entrydate.data
    #return render_template('updatebooking.html', form = form, message=[selected_date])  
    
    if not selected_date is None:
        sval =10000*selected_date.year + 100*selected_date.month + selected_date.day
        tval =10000*datetime.date.today().year + 100*datetime.date.today().month + datetime.date.today().day
        is_date_right = is_date_right and sval > tval and selected_date.weekday()<5
        error = "Selected day must later than today between Monday to Friday."
    else:
        is_date_right =False
        error = "No date is selected. Selected day must later than today between Monday to Friday."

    weekday =['Monday','Tuesday', 'Wednesday', 'Thursday','Friday']
    
    if form.update.data and is_date_right :# and form.validate_on_submit():
        customer = Customers.query.filter_by(id = session['appointment'][3]).first()
        name = customer.first_name +" "+customer.last_name##
        ###
        appointment.date =form.entrydate.data
        appointment.weekday = weekday[form.entrydate.data.weekday()]
        appointment.timeslot = form.timeslot.data
        appointment.customer_id = session['appointment'][3]
        appointment.country_id = Countries.query.filter_by(countryname=form.country.data).first().id
        appointment.vaccine_id = Vaccine.query.filter_by(vaccinename=form.vaccine.data).first().id 
        db.session.commit()
        session['from'] = 'update'
        session['original_app']= session['app_to_update']
        session['updated_app']= appointment.date.date().strftime('%d-%b-%Y') +" " +appointment.weekday+" " + appointment.timeslot+" "+\
                form.country.data +" "+form.vaccine.data
        session['id']=session['appointment'][3]
        session['initial']=True
        #return render_template('booking.html', form = form, message=app_list, msg='The appointment has been updated.') 
        return redirect(url_for('booking'))
    if form.cancel.data:
        session['from'] = 'update'
        session['original_app']= session['app_to_update']
        session['updated_app']= ""
        session['id']=session['appointment'][3]
        session['initial']=True
        return redirect(url_for('booking'))


    
     
    return render_template('updatebooking.html', form = form)



if __name__ == '__main__':
     app.run(debug=True, host='0.0.0.0') 