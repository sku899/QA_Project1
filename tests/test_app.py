#!/usr/bin/python3
import unittest
from flask import url_for, session
from flask_testing import TestCase

# import the app's classes and objects
from flask_app_db import app, db
from table_list import Customers, Countries, Vaccine, CVList, Bookings
from form_list import SignUpForm
from util_functions import get_country_list, get_vaccine_list, get_appointment_list, add_customer, is_exist, is_same_password
from datetime import date
from datetime import datetime
from wtforms.fields.html5 import DateField




# Create the base class
class TestBase(TestCase):
    def create_app(self):

        # Pass in testing configurations for the app. Here we use sqlite without a persistent database for our tests.
        app.config.update(SQLALCHEMY_DATABASE_URI="mysql+pymysql://me:qwerty123@localhost:3306/flaskdb",
                SECRET_KEY='TEST_SECRET_KEY',
                DEBUG=True
                )
        return app

    def setUp(self):
        """
        Will be called before every test
        """
        # Create table
        #db.create_all()
        db.drop_all()
        db.create_all()
        countries =['Argentina', 'Australia', 'Greece', 'India', 'South_Africa', 'Spain']
        vaccine_list =['Hepatitis_A', 'Hepatitis_B', 'Japanese_Encephalitis', 'Malaria', 'Measles', 'Rabies', 'Typhoid', 'Yellow_Fever']

        customer=Customers(first_name='John',last_name='Black', email='john.black@company.com', password='123456789',telephone='078123456',gender='M',age=30)
        db.session.add(customer)    
         
        vaccine_list_by_country=[
            ['Measles', 'Hepatitis_A', 'Typhoid', 'Hepatitis_B','Yellow_Fever', 'Rabies'],
            ['Measles',	'Hepatitis_B',	'Yellow_Fever'],
            ['Hepatitis_A',	'Hepatitis_B', 'Rabies'],
            ['Malaria', 'Hepatitis_A', 'Typhoid', 'Hepatitis_B', 'Japanese_Encephalitis', 'Rabies', 'Yellow_Fever'],
            ['Measles',	'Hepatitis_A', 'Typhoid', 'Hepatitis_B', 'Rabies', 'Yellow_Fever'],
            ['Measles',	'Hepatitis_A',	'Hepatitis_B']
            ]
        for v in vaccine_list:
            va=Vaccine(vaccinename = v)
            db.session.add(va)
            db.session.commit()


        for i, country in enumerate(countries):
            travel=Countries(countryname = country)
            db.session.add(travel)
            db.session.commit()
            vaccine =  vaccine_list_by_country[i]
        for v in vaccine:
            #print(country,v)
            countryid = Countries.query.filter_by(countryname=country).first()
            vaccineid = Vaccine.query.filter_by(vaccinename=v).first()
            print(countryid.id, '', vaccineid.id)
            
            item = CVList(country_id = countryid.id, vaccine_id = vaccineid.id)
            db.session.add(item)
            db.session.commit()

        booking =Bookings(date= datetime.now(), weekday='Monday', timeslot='9:30am', customer_id=1, country_id=6, vaccine_id=5)
        db.session.add(booking)

        # # Create test registree
        # sample1 = Register(name="MissWoman")

        # # save users to database
        # db.session.add(sample1)
        # db.session.commit()

    def tearDown(self):
        """
        Will be called after every test
        """

        db.session.remove()
        

# Write a test class for testing that the home page loads but we are not able to run a get request for delete and update routes.
class TestViews(TestBase):

    def test_login_get(self):
        response = self.client.get(url_for('login'))
        self.assertEqual(response.status_code, 200)

    def test_signup_get(self):
        response = self.client.get(url_for('signup',email='abc@cde.com'))
        self.assertEqual(response.status_code,200)

    #########
    def test_actions_get(self):
        response = self.client.get(url_for('actions',email='john.black@company.com', source="Hi" ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_booking_get(self):
        response = self.client.get(url_for('booking',email='john.black@company.com', oldapp="No App" ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)


    def test_update_get(self):
        response = self.client.get(url_for('update',email='john.black@company.com'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    # def test_updatebooking_get(self):
    #     response = self.app.get('/actions', query_string=dict())
    #     #response = self.client.get(url_for('actions'))
    #     self.assertEqual(response.status_code,200)

# class test_login(TestBase):
#     def test_login_post(self):
#         self.client.post(url_for('updatebooking'),data = dict(id='1', oldapp='old appointment'), follow_redirects=True)
#         response = self.client.get(url_for('booking'))
#         self.assertEqual(b'1', response.data)



# Test adding 
class Testlogin(TestBase):
    def test_add_post(self):
        response = self.client.post(
            url_for('login'),
            data = dict({'email': 'john.doe', 'password': '123456'}),
            follow_redirects=True
        )
        self.assertIn(b'Login',response.data)

# Test updating, this one might have problem

class TestSignup(TestBase):
    def test_update_post(self):
        self.client.post(
            url_for('signup', email ="John.doe@company.com"),
            follow_redirects=True
            )
        response = self.client.post(url_for('update',email= 'john.black@company.com' ))
        self.assertEqual(response.status_code,200)
        
# Test Deleting





###########################
class TestActions(TestBase):
    def test_actions_post(self):
        self.client.post(
            url_for('actions',email='john.black@company.com', source='welcome'),
            follow_redirects=True
        )
        response = self.client.get(url_for('booking',email= 'john.black@company.com',oldapp='no app'))
        print(response.status_code)
        self.assertEqual(response.status_code,200)

    def test_actions_post2(self):
        self.client.post(
            url_for('actions',email='john.black@company.com', source='welcome'),
            follow_redirects=True
        )
        response = self.client.get(url_for('update',email= 'john.black@company.com'))
        print(response.status_code)
        self.assertEqual(response.status_code,200)


class Testbooking(TestBase):
    def test_booking_post(self):
        booking = Bookings.query.first()
        self.client.post(
            url_for('booking',email= 'john.black@company.com',oldapp='no app'),
            follow_redirects=True
        )
        response = self.client.get(url_for('updatebooking',id =booking.id,oldapp='no app' ), follow_redirects=True)
        self.assertEqual(response.status_code,200)

    def test_booking_post2(self):
        self.client.post(
            url_for('booking',email= 'john.black@company.com',oldapp='no app')
        )
        response = self.client.get(url_for('booking',email= 'john.black@company.com',oldapp='no app' ), follow_redirects=True)
        self.assertEqual(response.status_code,200)



class Testupdatebooking(TestBase):
    def test_updatebooking_post(self):
        self.client.post(
            url_for('updatebooking', id ='1', oldapp="No App" ),
            follow_redirects=True
            )
        response =  self.client.get(url_for('booking', email='john.black@company.com',oldapp="no app"))
        self.assertEqual(response.status_code,200)

def test_get_country_list():
    country= get_country_list()
    assert 'Greece'in country


def test_get_vaccine_list():
    vaccine= get_vaccine_list('Spain')
    assert 'Hepatitis_A'in vaccine


def test_appointment_list():
    result = get_appointment_list([])
    assert "You don't have any appointment yet." in result 


def test_signup():
    frm = SignUpForm
    frm.firstname.data = "John"
    frm.lastname.data = "Black"
    frm.email.data ="john.black@example.com"
    frm.password.data ="123456"
    frm.telephone.data ="0789123"
    frm.gender.data = "M"
    frm.age.data =30
    customer = add_customer(frm)
    assert customer.email ==  "john.black@example.com"
    customers = Customers.query.all()
    email = "john.black2@example.com"
    result = is_exist(customers, email)
    assert result == False
    result = is_same_password(customers, "1234567", email)
    assert result == False




    
        

   