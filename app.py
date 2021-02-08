from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, flash, session, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, validators
from wtforms.fields.html5 import DateField
import datetime
# from wtforms import DataRequired, ValidationError,Email, Length
import form_list as frm
from flask_app_db import db, app
from table_list import Customers, Countries, Vaccine, CVList, Bookings
from util_functions import *



@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def login():
    form = frm.LoginForm()
    email = form.email.data
    password = form.password.data
    if form.register.data:
        if not len(email)>0:
            email = 'No email'
        return redirect(url_for('signup',email=email))
    if  not form.validate_on_submit():        
        if form.email.errors:
            email=''
        if form.password.errors:
            password=''
        form.email.data = email
        form.password.data = password
        return render_template('login.html', form = form)
    else:
        if is_exist(Customers.query.all(), form.email.data): ## return customer
            ##login successfully
            if is_same_password(Customers.query.all(), form.password.data, form.email.data):
                # return render_template('login.html', form = form,message = "existing customer with correct password")
                return redirect(url_for('actions', email=email, source='Welcome come back'))
            else:
                form.email.data = email=''
                return render_template('login.html', form = form, message = '**Password is incorrect. Please try again.' )
        else: # new user
            form.email.data = email
            return render_template('login.html', form = form, message = '**New User?? Please Register to Create your Account.' )


@app.route('/actions/<email>/<source>', methods=['GET', 'POST'])
def actions(email, source):
    form = frm.ActionsForm()
    customer = Customers.query.filter_by(email = email).first()
    title = f"{source}, {customer.first_name+' '+customer.last_name}, you can view your account details and book an appointment."
    appointments = Bookings.query.filter_by(customer_id=customer.id).order_by(Bookings.date).all()
    appointment_list = get_appointment_list(appointments)
    if form.booking.data:
        return redirect(url_for('booking',email=email, oldapp='no app'))
    if form.update.data:
        return redirect(url_for('update', email =email ))
    if form.logout.data:
        return redirect(url_for('login'))  
    return render_template('actions.html', form = form, title=title, message=appointment_list) 
    

@app.route('/signup/<email>', methods=['GET', 'POST'])
def signup(email):
    form = frm.SignUpForm()
    errmsg=""
    if '@' in  email:
            form.email.data = email  
            email= ''  
    if  form.validate_on_submit(): ## everything is OK
        email =  form.email.data
        if is_exist(Customers.query.all(), form.email.data):
            #return render_template('signup.html', form = form,message = 'Existing customer')
            return redirect(url_for('login'))
        else:
            customer = add_customer(form)
            #customer.password = currentpaessword
            db.session.add(customer)
            name = form.firstname.data +" " +form.lastname.data #customer.first_name +" "+ customer.last_name
            db.session.commit()
            output_message = f"Hi {name}, your account has been added. Here is your details."
            return redirect(url_for('update', email=email))
            #return render_template('update.html', form = form,message = output_message)
    else:
        errmsg = 'Please check your data. All fields are required'
    return render_template('signup.html', form = form , message = errmsg)
    #return render_template('signup.html', form = form)


@app.route('/update/<email>', methods=['GET', 'POST'])
def update(email):
    form = frm.UpdateForm()
    customer = Customers.query.filter_by(email=email).first()
    if form.update.data and form.validate_on_submit(): ##update record
        customer.first_name =form.firstname.data
        customer.last_name = form.lastname.data 
        customer.email = form.email.data
        customer.telephone = form.telephone.data
        customer.gender = form.gender.data
        customer.age = form.age.data
        db.session.commit()
        name = form.firstname.data +" "+form.lastname.data
        return render_template('update.html', form = form, customer = name,greeting='Hi',message = 'your account has been update record successfully.')
    elif form.delete.data:
        num_of_apps = len(Bookings.query.filter_by(customer_id=customer.id).all())
        name = form.firstname.data +" "+form.lastname.data
        if num_of_apps ==0:
            db.session.delete(customer)
            db.session.commit()            
            return f"Hi {name}, your account has been deleted.<br/>"
        else:
            return render_template('update.html', form = form, customer = name,message = f'You have {num_of_apps} appointment(s) with us. You cannot withdraw the account now.')
    else:
        form.firstname.data = customer.first_name
        form.lastname.data = customer.last_name
        form.email.data = customer.email
        form.telephone.data = customer.telephone
        form.gender.data = customer.gender
        form.age.data = customer.age
        name = customer.first_name +" "+customer.last_name
    if form.booking.data:
        return redirect(url_for('booking', email=email,oldapp='no app'))
    name = form.firstname.data +" "+form.lastname.data
    return render_template('update.html', form = form, customer = name,greeting='Hi')


@app.route('/booking/<email>/<oldapp>', methods=['GET', 'POST'])
def booking(email,oldapp):
    form = frm.BookingForm()
    customer = Customers.query.filter_by(email=email).first()
    #display all appointments
    appointments = Bookings.query.filter_by(customer_id=customer.id).order_by(Bookings.date).all()
    app_list = get_appointment_list(appointments)
    form.appointments.choices = app_list[0:1] +app_list[2:]
    #populate country and vaccine drop down menus
    country_list = get_country_list()
    form.country.choices = country_list
    selected_country = country_list[0]
    vaccine_list = get_vaccine_list(selected_country)
    form.vaccine.choices = vaccine_list
    if form.entrydate.data is None:
        form.entrydate.data = datetime.date.today()
    if form.go.data:
        selected_country = form.country.data
        vaccine_list = get_vaccine_list(selected_country)
        form.vaccine.choices = vaccine_list
    #create a new appointment
    if form.create.data:
        is_date_right = True
        error = ""
        selected_date = form.entrydate.data
        if not selected_date is None:
            is_date_right = is_date_right and selected_date > datetime.date.today() and selected_date.weekday()<5
            error = "Selected day must later than today between Monday to Friday."
        else:
            is_date_right =False
            error = "No date is selected. Selected day must later than today between Monday to Friday."
        is_vaccine_selected = True
        if form.vaccine.data is None:
            error += "No vaccine is selected. Press 'Go' button to enable selection"
            is_vaccine_selected = False
        weekday =['Monday','Tuesday', 'Wednesday', 'Thursday','Friday']
        if is_date_right and is_vaccine_selected:# and form.validate_on_submit():
            #customer = Customers.query.filter_by(id = session['id']).first()
            name = customer.first_name +" "+customer.last_name##            
            ###
            date = selected_date
            weekday = weekday[selected_date.weekday()]
            timeslot = form.timeslot.data
            customer_id = customer.id
            country_id = Countries.query.filter_by(countryname=form.country.data).first().id
            vaccine_id = Vaccine.query.filter_by(vaccinename=form.vaccine.data).first().id 
            booking_to_add = Bookings(date=date, weekday=weekday, timeslot = timeslot,customer_id=customer_id, country_id= country_id, vaccine_id=vaccine_id)
            db.session.add(booking_to_add)
            db.session.commit()
            appointments = Bookings.query.filter_by(customer_id=customer.id).order_by(Bookings.date).all()
            app_list = get_appointment_list(appointments)
            form.appointments.choices = app_list[0:1] +app_list[2:]
            return render_template('booking.html', form = form, message = app_list,msg = app_list[-1] + " has been added." )
        else:
            errmsg ="**error: "
            if not is_date_right:
                errmsg += "Selected date must be a working day later than today. "
            if not is_vaccine_selected:
                errmsg += "Make sure vaccine is selected."
            return render_template('booking.html', form = form, message = app_list,msg = errmsg )#errmsg )

        #delete an appointment
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
                appointments = Bookings.query.filter_by(customer_id=customer.id).order_by(Bookings.date).all()
                app_list = get_appointment_list(appointments)
                form.appointments.choices = app_list[0:1] +app_list[2:]
                return render_template('booking.html', form = form, message = app_list ,msg = delete_appointment + " has been deleted.")
            else:
                return redirect(url_for('updatebooking',id=appointments_to_delete.id, oldapp =delete_appointment ))
        else:
            return render_template('booking.html', form = form, message=app_list, msg='**error: No appointment is selected.') 
    # if session['from'] == 'update':
    #     msg = session['original_app'] + " has been changed to " + session['updated_app']+"."
    #     if session['updated_app']=='':
    #         msg = session['original_app'] + " is not changed. "
    #     session['from']=''
    if form.back.data:
        return redirect(url_for('actions',email=customer.email,source='Welcome back'))
    msg=''
    if not oldapp == 'no app':
        msg = oldapp 
    
    return render_template('booking.html', form = form, message=app_list, msg=msg)  
    #return render_template('update.html', form = form)


@app.route('/updatebooking/<id>/<oldapp>', methods=[ 'POST', 'GET'])
def updatebooking(id,oldapp):
    form=frm.UpdateBookingForm()
    appointment_id = int(id)
    appointment=Bookings.query.filter_by(id = appointment_id).first()

    country_list= get_country_list()
    form.country.choices =country_list
    if form.country.data is None:
        form.country.data = Countries.query.filter_by(id = appointment.country_id).first().countryname
        vaccine_list=get_vaccine_list(form.country.data)
        form.vaccine.choices = vaccine_list
        form.vaccine.data = Vaccine.query.filter_by(id = appointment.vaccine_id).first().vaccinename
        form.entrydate.data = appointment.date
        form.timeslot.data=appointment.timeslot
    if form.go.data:
        vaccine_list=get_vaccine_list(form.country.data)
        form.vaccine.choices = vaccine_list
        form.vaccine.data = Vaccine.query.filter_by(id = appointment.vaccine_id).first().vaccinename
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
        customer = Customers.query.filter_by(id = appointment.customer_id).first()
        name = customer.first_name +" "+customer.last_name##
        ###
        appointment.date =form.entrydate.data
        appointment.weekday = weekday[form.entrydate.data.weekday()]
        appointment.timeslot = form.timeslot.data
        appointment.customer_id = customer.id
        appointment.country_id = Countries.query.filter_by(countryname=form.country.data).first().id
        appointment.vaccine_id = Vaccine.query.filter_by(vaccinename=form.vaccine.data).first().id 
        db.session.commit()
        email= customer.email
        #return render_template('booking.html', form = form, message=app_list, msg='The appointment has been updated.') 
        oldapp += ' has been changed to '+ str(appointment.date.strftime('%d-%b-%Y')) +' '+appointment.weekday+' '+appointment.timeslot+' '+\
            form.country.data+' '+ form.vaccine.data

        return redirect(url_for('booking',email=email,oldapp=oldapp))
    if form.cancel.data:
        email= Customers.query.filter_by(id = appointment.customer_id).first().email
        return redirect(url_for('booking',email=email,oldapp=oldapp + ' has not been changed.'))
    return render_template('updatebooking.html', form = form)



if __name__ == '__main__':
     app.run(debug=True, host='0.0.0.0') 