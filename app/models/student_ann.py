#!/usr/bin/env python3

# Import
from flask_sqlalchemy import SQLAlchemy
from app.app import db
from datetime import datetime
from sqlalchemy import ForeignKey
import re
from sqlalchemy import UniqueConstraint



class Student_ann(db.Model):
    '''
    A class that defines the Student Announcement
    '''
    __tablename__ = 'students_annt'
    stud_ann_id = db.Column(db.Integer, primary_key=True, nullable=True)
    ann_id = db.Column(db.Integer, db.foreignKey('announcements.announcement_id'), nullable=False)
    admission_number = db.Column(db.Integer, db.foreignKey('students.admission_number'), nullable=False)
    read_status = db.Column(db.Boolean, default=False, nullable=False)
