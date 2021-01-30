'''
This file will create the tables which show in app.py with or without records
'''

from app import db, Users, Customers, Countries, Vaccine  , CVList

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









# testuser = Users(first_name='Grooty',last_name='Toot') # Extra: this section populates the table with an example entry
# db.session.add(testuser)
# db.session.commit()

# customer = Customers(first_name ='John',last_name ='Dow',email = 'john.dow@company.com',telephone ='1234567',gender = 'M',age =20)
# db.session.add(customer)
# db.session.commit()
