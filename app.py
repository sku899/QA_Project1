from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, validators
# from wtforms import DataRequired, ValidationError,Email, Length

app = Flask(__name__)
app.config['SECRET_KEY'] = 'YOUR_SECRET_KEY'
username='me'
password = 'qwerty123'
localhost = 'localhost:3306'
database = 'flaskdb'

app.config["SQLALCHEMY_DATABASE_URI"] = f'mysql+pymysql://{username}:{password}@{localhost}/{database}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app)

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

###form setup
class LoginForm(FlaskForm):
    email = StringField('email',validators=[validators.Email(granular_message=True)])
    password = PasswordField('password', validators=[validators.Length(min=6,max=25)])
    submit = SubmitField('Sign In')


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def register():
    error = ""
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        return render_template('login.html', form = form, email=email)
    else:
        return render_template('login.html', form = form, email="")
        

    return render_template('login.html', form=form, message = form.email.process_errors)

if __name__ == '__main__':
     app.run(debug=True, host='0.0.0.0')