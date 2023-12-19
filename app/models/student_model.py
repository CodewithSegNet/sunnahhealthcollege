#!/usr/bin/env python3

# Import
import app.models.course_model
from app.models.department_model import Department
from app.app import db
from app.models.student_record import StudentRecord
from datetime import datetime
import re
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash




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
    admission_number = db.Column(db.String(50), primary_key=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    department_level = db.Column(db.Integer, db.ForeignKey('departments.department_level'), nullable=False)
    department_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    phone_number = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

     # Define a relationship with the Course model through the association table
    courses = db.relationship('Course', secondary=student_courses_association, backref=db.backref('students', lazy=True))

    department = db.relationship('Department', backref='related_students', overlaps="related_department.department_level")


    
    # Add a relationship to the historical department level
    department_history = db.relationship('StudentRecord', backref='student', lazy='dynamic')



    def change_department_level(self, new_level):
        # Save current level to history
        history_record = StudentRecord(admission_number=self.admission_number, department_level=self.department_level)
        db.session.add(history_record)

        # Update current level
        self.department_level = new_level
        db.session.commit()


    # A validation check for email format using python library 'validate_email'
    def validate_email(self, email):
        '''
        define a re expression for a simple email format check
        '''
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_pattern, email):
            raise ValueError("Invalid email format")