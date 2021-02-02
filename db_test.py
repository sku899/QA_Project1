from app import Customers, db
 
 
def test_new_user():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, hashed_password, authenticated, and role fields are defined correctly
    """
    customer=Customers(first_name='John',last_name='Black', email='john.black@company.com', password='123456789',telephone='078123456',gender='M',age=30)
    db.session.add(customer)
    user = User('patkennedy79@gmail.com', 'FlaskIsAwesome')
    assert customer.first_name == 'John'
    assert customer.las_name == 'Black'


    #     id = db.Column(db.Integer, primary_key=True)
    # first_name = db.Column(db.String(30), nullable=False)
    # last_name = db.Column(db.String(30), nullable=False)
    # email = db.Column(db.String(60), nullable=False)
    # password = db.Column(db.String(60), nullable=False)
    # telephone = db.Column(db.String(12), nullable=False)
    # gender = db.Column(db.String(2), nullable=False)
    # age = db.Column(db.Integer, nullable=False)
    # booking = db.relationship('Bookings', backref='customers')