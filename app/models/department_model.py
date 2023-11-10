#!/usr/bin/env python3

# Import
from app.app import db




class Department(db.Model):
    '''
    A class that defines the Student Department
    '''
    __tablename__ = 'departments'
    department_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    department_name = db.Column(db.Sting(255), nullable=False, unique=True)


    # Constructor to initialize Student Object with attributes.
    def __init__(self, department_name):
        self.department_name = department_name
  