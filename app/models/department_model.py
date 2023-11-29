#!/usr/bin/env python3

# Import
from app.app import db




class Department(db.Model):
    '''
    A class that defines the Student Department
    '''
    __tablename__ = 'departments'
    department_level = db.Column(db.Integer, primary_key=True, nullable=False)
    department_name = db.Column(db.String(255), nullable=False, unique=True)


    students = db.relationship('Student', backref='related_department', overlaps="related_department.department_level")