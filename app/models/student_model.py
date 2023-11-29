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
    db.Column('admission_number', db.String(20), db.ForeignKey('students.admission_number')),
    db.Column('course_title', db.String(255), db.ForeignKey('courses.course_title')),
    db.Column('course_code', db.String(20), nullable=True),
)



class Student(db.Model):
    '''
    A class that defines the Student Description
    '''
    __tablename__ = 'students'
    admission_number = db.Column(db.String(20), primary_key=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    department_level = db.Column(db.Integer, db.ForeignKey('departments.department_level'), nullable=False)
    department_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    phone_number = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

     # Define a relationship with the Course model through the association table
    courses = db.relationship('Course', secondary=student_courses_association, backref=db.backref('students', lazy=True))

    department = db.relationship('Department', backref='related_students', overlaps="related_department.department_level")


    # A validation check for email format using python library 'validate_email'
    def validate_email(self, email):
        '''
        define a re expression for a simple email format check
        '''
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_pattern, email):
            raise ValueError("Invalid email format")