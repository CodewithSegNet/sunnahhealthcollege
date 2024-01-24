#!/usr/bin/env python3

# Import
from app import db
from models.department_model import Department
import models.student_model
from models.semester import Semester
from sqlalchemy.orm import relationship


class Course(db.Model):
    '''
    A class that defines the Course Description
    '''
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    course_code = db.Column(db.String(20), nullable=False)
    student_id = db.Column(db.String(50), db.ForeignKey('students.admission_number'), nullable=False)
    course_title = db.Column(db.String(255), nullable=False)
    credit = db.Column(db.Integer, nullable=False)
    ca_score = db.Column(db.Integer, nullable=True)
    exam_score = db.Column(db.Integer, nullable=True)
    total_score = db.Column(db.Integer, nullable=True)
    grade = db.Column(db.String(5), nullable=True)
    remark = db.Column(db.String(255), nullable=True)
