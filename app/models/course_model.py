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
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.department_id'), nullable=False)
    course_title = db.Column(db.String(255), nullable=False)
    course_code = db.Column(db.String(20), nullable=False, unique=True)
    

    # Define a relationship with the Department model
    department = db.relationship('Department', backref=db.backref('courses', lazy=True))

    # Constructor to initialize Course Object with attributes.
    def __init__(self, department_id, course_title, course_code):
        self.department_id = department_id
        self.course_title = course_title
        self.course_code = course_code
