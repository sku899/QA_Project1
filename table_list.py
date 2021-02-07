from flask_app_db import db
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