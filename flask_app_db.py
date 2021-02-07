'''
this file create flask app and db
'''

from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'YOUR_SECRET_KEY'
username='me'
password = 'qwerty123'
ocalhost = 'localhost:3306'
database = 'flaskdb'

#app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{username}:{password}@{localhost}/{database}"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:12345@localhost:3306/flaskdb"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app)
