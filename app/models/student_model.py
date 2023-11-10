#!/usr/bin/env python3

# Import
from datetime import datetime
import re
from app.app import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from app.department_model import Department


class Student(db.Model):
    '''
    A class that defines the Student Description
    '''
    __tablename__ = 'students'
    admission_number = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=True)
    name = db.Column(db.String(255), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('Department.department_id'), nullable=False)
    department_level = db.Column(db.String(3), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    phone_number = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


    # Define a relationship with the Role model
    role = db.relationship('Role', backref=db.backref('students', lazy=True))


    # Constructor to initialize Student Object with attributes.
    def __init__(self, name, date_of_birth, department_id, department_level, email, phone_number, role_id):
        self.name = name
        self.date_of_birth = date_of_birth
        self.department_id = department_id
        self.department_level = department_level
        self.email = email
        self.phone_number = phone_number
        self.role_id = role_id
    


    # A validation check for email format using python library 'validate_email'
    def validate_email(self, email):
        '''
        define a re expression for a simple email format check
        '''
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_pattern, email):
            raise ValueError("Invalid email format")