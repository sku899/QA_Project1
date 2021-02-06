#!/usr/bin/python3
import unittest
from flask import url_for, session
from flask_testing import TestCase

# import the app's classes and objects
from flask_app_db import app, db
from table_list import Customers, Countries, Vaccine, CVList, Bookings



# Create the base class
class TestBase(TestCase):
    def create_app(self):

        # Pass in testing configurations for the app. Here we use sqlite without a persistent database for our tests.
        app.config.update(SQLALCHEMY_DATABASE_URI="mysql+pymysql://me:qwerty123@localhost:3306/testdb",
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
        countries =['Argentia', 'Australia', 'Greece', 'India', 'South_Africa', 'Spain']
        vaccine_list =['Hepatitis_A', 'Hepatitis_B', 'Japanese_Encephalitis', 'Malaria', 'Measles', 'Rabies', 'Typhoid', 'Yellow_Fever']
            
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
        session['count'] = 1
        response = self.client.get(url_for('signup',email='abc@cde.com'))
        self.assertEqual(response.status_code,200)

    # def test_updatebooking_get(self):
    #     response = self.app.get('/actions', query_string=dict())
    #     #response = self.client.get(url_for('actions'))
    #     self.assertEqual(response.status_code,200)

# Test adding 
class Testlogin(TestBase):
    def test_add_post(self):
        response = self.client.post(
            url_for('login'),
            data = dict({'email': 'john.doe', 'password': '123456'}),
            follow_redirects=True
        )
        self.assertIn(b'Login',response.data)

# Test updating

class TestSignup(TestBase):
    def test_update_post(self):
        self.client.updatebooking(id=1 , oldapp="You don't have appointment")
        response = self.client.post(
            url_for('updatebooking'),
            data =dict(id=1 , oldapp="You don't have appointment"),
            follow_redirects=True
            )
        self.assertEqual(response.status_code,200)
        print(response.status_code)
# Test Deleting

class TestActions(TestBase):
    def test_actions_post(self):
        
        response = self.client.post(
            url_for('actions'),
            data = dict(email='john.doe@company.com', source='welcome'),
            follow_redirects=True
            )
        print(response.status_code)
        self.assertEqual(response.status_code,200)
        

   