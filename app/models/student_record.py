#!/usr/bin/env python3

# Import
from app.app import db
from datetime import datetime


class StudentRecord(db.Model):
    '''
    A class that defines the history of Student Department Levels
    '''
    __tablename__ = 'student_department_history'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    admission_number = db.Column(db.String(50), db.ForeignKey('students.admission_number'), nullable=False)
    department_level = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    semester = db.Column(db.Integer, db.ForeignKey('semesters.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
