'''
This file will create the tables which show in app.py with or without records
'''

from app import db, Users, Customers


db.create_all()

testuser = Users(first_name='Grooty',last_name='Toot') # Extra: this section populates the table with an example entry
db.session.add(testuser)
db.session.commit()

customer = Customers(first_name ='John',last_name ='Dow',email = 'john.dow@company.com',telephone ='1234567',gender = 'M',age =20)
db.session.add(customer)
db.session.commit()
