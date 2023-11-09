#!/usr/bin/env python3

# Import
from flask_sqlalchemy import SQLAlchemy
from app.app import db
from datetime import datetime
from sqlalchemy import ForeignKey
import re
from sqlalchemy import UniqueConstraint



class student(db.Model):
    '''
    A class that defines the Student Description
    '''
    __tablename__ = 'students'
    Admission_Number = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=True)
    Name = db.Column(db.String(255), nullable=False)
    Date_of_birth = db.Column(db.Date, nullable=False)
    Department_id = db.Column(db.Integer, db.foreignKey('departments.Department_id'), nullable=False)
    Department_level = db.Column(db.String(3), nullable=False)
    Email = db.Column(db.String(255), nullable=False, unique=True)
    Phone_number = db.Column(db.String(20), nullable=False)
    Created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    Updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


    # Constructor to initialize Student Object with attributes.
    def __init__(self, Name, Date_of_birth, Department_id, Department_level, Email, Phone_number):
        self.Name = Name
        self.Date_of_birth = Date_of_birth
        self.Department_id = Department_id
        self.Department_level = Department_level
        self.Email = Email
        self.Phone_number = Phone_number
    


    # A validation check for email format using python library 'validate_email'
    def validate_email(self, email):
        '''
        define a re expression for a simple email format check
        '''
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_pattern, email):
            raise ValueError("Invalid email format")