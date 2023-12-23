#!/usr/bin/env python3

# Import
from app.app import db
from app.models.department_model import Department
import app.models.student_model
from app.models.semester import Semester
from sqlalchemy.orm import relationship


class Course(db.Model):
    '''
    A class that defines the Course Description
    '''
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    course_title = db.Column(db.String(255), nullable=False)
    course_code = db.Column(db.String(20), nullable=False)
    credit = db.Column(db.Integer, nullable=False)
    student_id = db.Column(db.String, db.ForeignKey('students.admission_number'))

