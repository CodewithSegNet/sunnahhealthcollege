#!/usr/bin/env python3

# Import
from models.course_model import Course
from models.department_model import Department
from app import db
from models.student_record import StudentRecord
from datetime import datetime
import re
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash


class Student(db.Model):
    '''
    A class that defines the Student Description
    '''
    __tablename__ = 'students'
    admission_number = db.Column(db.String(50), primary_key=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=True)
    date_of_birth = db.Column(db.Date, nullable=True)
    state = db.Column(db.String(20), nullable=True)
    gender = db.Column(db.String(20), nullable=True)
    department_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=True, unique=True)
    phone_number = db.Column(db.String(20), nullable=True)
    image_data = db.Column(db.LargeBinary)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
  

    # Relationship with department
    departments = db.relationship('Department', backref='students')


    # Relationship with Course
    courses = db.relationship('Course', backref='students')

     # Relationship with semester
    semesters = db.relationship('Semester', backref='students')

  




   

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


    # A validation check for email format using python library 'validate_email'
    def validate_email(self, email):
        '''
        define a re expression for a simple email format check
        '''
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_pattern, email):
            raise ValueError("Invalid email format")