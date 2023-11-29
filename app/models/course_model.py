#!/usr/bin/env python3

# Import
from app.app import db
from app.models.department_model import Department
from sqlalchemy.orm import relationship


class Course(db.Model):
    '''
    A class that defines the Course Description
    '''
    __tablename__ = 'courses'
    course_title = db.Column(db.String(255), primary_key=True, nullable=False)
    department_level = db.Column(db.Integer, db.ForeignKey('departments.department_level'), nullable=False)
    course_code = db.Column(db.String(20), nullable=False, unique=True)
    

    # Define a relationship with the Department model
    department = db.relationship('Department', backref=db.backref('courses', lazy=True))
