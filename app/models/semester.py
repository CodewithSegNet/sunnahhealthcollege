#!/usr/bin/env python3

# Import
from app.app import db


class Semester(db.Model):
    '''
    A class that defines the Semester Description
    '''
    __tablename__ = 'semesters'
    semester = db.Column(db.String(50), primary_key=True)
