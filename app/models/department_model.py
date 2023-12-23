#!/usr/bin/env python3

# Import
from app.app import db
import app.models.student_model
from app.models.semester import Semester
from sqlalchemy.orm import relationship




class Department(db.Model):
    '''
    A class that defines the Student Department
    '''
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    department_level = db.Column(db.Integer, nullable=False)
    department_name = db.Column(db.String(255), nullable=False)
    student_id = db.Column(db.String, db.ForeignKey('students.admission_number'), nullable=False)


