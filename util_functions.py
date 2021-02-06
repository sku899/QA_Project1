from table_list import Customers, Countries, Vaccine, CVList, Bookings
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

def get_country_list():
    allcountries = Countries.query.all()
    country_list=[]
    for country in allcountries:
        country_list.append(country.__dict__["countryname"])
    return country_list


def get_vaccine_list(selected_country):
    country_id = Countries.query.filter_by(countryname = selected_country).first().id
    vaccine_list=[]
    selected_country_vaccine = CVList.query.filter_by(country_id = country_id).all()
    for v in selected_country_vaccine:
        vaccine_list.append(Vaccine.query.filter_by(id = v.vaccine_id).first().vaccinename)
    return vaccine_list
    