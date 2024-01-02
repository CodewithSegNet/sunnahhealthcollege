#!/usr/bin/env python3

# Import
from app.app import db
import app.models.student_model
from sqlalchemy.orm import relationship



class Semester(db.Model):
    '''
    A class that defines the Semester Description
    '''
    __tablename__ = 'semesters'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    semester = db.Column(db.String(20), nullable=False)
    student_id = db.Column(db.String(50), db.ForeignKey('students.admission_number'), nullable=False)
