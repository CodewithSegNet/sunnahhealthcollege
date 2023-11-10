#!/usr/bin/env python3

# Import
from datetime import datetime
import re
from app.app import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from app.models.department_model import Department
from sqlalchemy.orm import relationship
import app.models.course_model 



# Association Table for the many-to-many relationship
student_courses_association = db.Table('student_courses_association',
    db.Column('admission_number', db.Integer, db.ForeignKey('students.admission_number')),
    db.Column('course_id', db.Integer, db.ForeignKey('courses.id')),
    db.Column('course_title', db.String(255), nullable=True),
)



class Student(db.Model):
    '''
    A class that defines the Student Description
    '''
    __tablename__ = 'students'
    admission_number = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=True)
    name = db.Column(db.String(255), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.department_id'), nullable=False)
    department_level = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    phone_number = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

     # Define a relationship with the Course model through the association table
    courses = db.relationship('Course', secondary=student_courses_association, backref=db.backref('students', lazy=True))


    # Constructor to initialize Student Object with attributes.
    def __init__(self, name, date_of_birth, department_id, department_level, email, phone_number):
        self.name = name
        self.date_of_birth = date_of_birth
        self.department_id = department_id
        self.department_level = department_level
        self.email = email
        self.phone_number = phone_number
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    


    # A validation check for email format using python library 'validate_email'
    def validate_email(self, email):
        '''
        define a re expression for a simple email format check
        '''
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_pattern, email):
            raise ValueError("Invalid email format")