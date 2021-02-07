from test_app import db
from app import Customers, Countries, Vaccine, CVList, Bookings

def create_table():
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