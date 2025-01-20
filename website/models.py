from . import db
from datetime import date
from sqlalchemy.orm import validates

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    registration_code = db.Column(db.String(7), unique=True, nullable=False)
    foundation_date = db.Column(db.Date, default=date.today, nullable=False)
    capital = db.Column(db.Integer, nullable=False)
    owners = db.relationship('Owner', backref='company', lazy=True)

    @validates('name')
    def validate_name(self, key, value):
        existing_company = Company.query.filter_by(name=value).first()

        if existing_company:
            raise ValueError("This company name already exists.")
        if len(value) < 3 or len(value) > 100:
            raise ValueError("Company name must be 3-100 characters.")
        return value

    @validates('registration_code')
    def validate_registration_code(self, key, value):
        existing_company = Company.query.filter_by(registration_code=value).first()
        
        if existing_company:
            raise ValueError("This registration code already exists.")
        if len(value) != 7:
            raise ValueError("Registration code must be 7 numbers.")
        return value
    
    @validates('foundation_date')
    def validate_foundation_date(self, key, value):
        if value > date.today():
            raise ValueError("Foundation date can't be in the future.")
        return value

    @validates('capital')
    def validate_capital(self, key, value):
        if value < 2500:
            raise ValueError("Capital must be more than 2499.")
        return value
    
class Owner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_type = db.Column(db.String(10), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    personal_id = db.Column(db.String(11), nullable=False)
    share_amount = db.Column(db.Integer,default=0, nullable=False)
    is_founder = db.Column(db.Boolean, default=True, nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False, index=True)

    @validates('first_name')
    def validate_first_name(self, key, value):
        if len(value) > 20 or len(value) < 3:
            raise ValueError("First name must be 3-20 characters.")
        return value
    
    @validates('last_name')
    def validate_last_name(self, key, value):
        if len(value) > 20 or len(value) < 3:
            raise ValueError("Last name must be 3-20 characters.")
        return value
    
    @validates('personal_id')
    def validate_personal_id(self, key, value):
        if len(value) != 11:
            print(len(value))
            raise ValueError("ID code must be 11 numbers.")
        return value
    
