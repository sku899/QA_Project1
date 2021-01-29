from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, flash, session, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, validators
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

class SignUpForm(FlaskForm):
    firstname = StringField('First Name',validators=[validators.DataRequired()])
    lastname = StringField('Last Name',validators=[validators.DataRequired()])
    email = StringField('email',validators=[validators.Email(granular_message=True)])
    password = PasswordField('Password', validators=[validators.EqualTo('reenterpassword',message = "Password doesn't match")])
    reenterpassword = PasswordField('Re-Type Password', validators=[validators.Length(min=6,max=25)])
    telephone = StringField('Telephone',validators=[validators.DataRequired()])
    gender = SelectField('Gender',choices=['M','F'])
    age = StringField('Age',validators=[validators.DataRequired()])
    submit = SubmitField('Sign Up')

class UpdateForm(FlaskForm):
    firstname = StringField('First Name',validators=[validators.DataRequired()])
    lastname = StringField('Last Name',validators=[validators.DataRequired()])
    email = StringField('email',validators=[validators.Email(granular_message=True)])
    telephone = StringField('Telephone',validators=[validators.DataRequired()])
    gender = SelectField('Gender',choices=['M','F'])
    age = StringField('Age',validators=[validators.DataRequired()])
    update = SubmitField('Update')
    delete = SubmitField('Delete')

####Functions
def is_exist(customers, email):
    for customer in customers:
        if (email == customer.email):
            return True
    return False

def is_same_password(customers, password, email):
    for customer in customers:
        if (email == customer.email) and (password == customer.password):
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


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def register():
    error = ""
    form = LoginForm()
    email = form.email.data
    password = form.password.data
    if  not form.validate_on_submit():        
        if form.email.errors:
            email=""
        if form.password.errors:
            password=""
        form.email.data = email
        form.password.data = password
        return render_template('login.html', form = form)
    else:
        if is_exist(Customers.query.all(), form.email.data):
            if is_same_password(Customers.query.all(), form.password.data, form.email.data):
                # return render_template('login.html', form = form,message = "existing customer with correct password")
                session['count'] = 1
                session['email'] = email
                return redirect(url_for('update'))
            else:
                return render_template('login.html', form = form,message = "Password is incorrect. Please try again.")

        else: # new user
            session['email'] =  email
            session['password'] = password
            session['count'] = 1
            return redirect(url_for('signup'))
    #return render_template('signup.html', form = form)
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    #currentpassword = form.password.data
    if session['count'] ==1:
        form.email.data = session.get('email')
        session['count'] = 2
    
    if  form.validate_on_submit(): ## everything is OK
        # if len(Customers.query.all()) ==0:
        #     return render_template('signup.html', form = form,message = 'New customer')
        # else:
        
        if is_exist(Customers.query.all(), form.email.data):
            return render_template('signup.html', form = form,message = 'Existing customer')
        else:
            customer = add_customer(form)
            #customer.password = currentpaessword
            db.session.add(customer)
            name = customer.first_name +" "+ customer.last_name
            db.session.commit()
            output_message = f"Hi {name}, your account has been added. Here is your details."
            
            return render_template('update.html', form = form,message = output_message)
    else:
        return render_template('signup.html', form = form , message = 'Please check your data')
    #return render_template('signup.html', form = form)


@app.route('/update', methods=['GET', 'POST'])
def update():
    form = UpdateForm()
    currentemail = session['email']
    customer = Customers.query.filter_by(email=session['email']).first()
    if session['count'] == 1:
        form.firstname.data = customer.first_name
        form.lastname.data = customer.last_name
        form.email.data = customer.email
        form.telephone.data = customer.telephone
        form.gender.data = customer.gender
        form.age.data = customer.age
        session['name']= customer.first_name +" "+customer.last_name
        session['count'] = 2
    if form.update.data and form.validate_on_submit(): ##update record
        customer.first_name =form.firstname.data
        form.lastname.data = customer.last_name
        customer.email = form.email.data
        customer.telephone = form.telephone.data
        customer.gender = form.gender.data
        customer.age = form.age.data
        db.session.commit()
        return render_template('update.html', form = form, message = 'Update record successfully.')
    if form.delete.data:
        db.session.delete(customer)
        db.session.commit()
        return f"Hi {session['name']}, your account has been deleted.<br/>"



    return render_template('update.html', form = form)



if __name__ == '__main__':
     app.run(debug=True, host='0.0.0.0')