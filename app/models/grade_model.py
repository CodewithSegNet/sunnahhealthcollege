#!/usr/bin/env python3


#  Import
from app.app import db
from app.models.student_model import Student
from app.models.course_model import Course

class Grade(db.Model):
    '''
    A class that defines the Grade Description
    '''
    __tablename__ = 'grades'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    student_admission_number = db.Column(db.Integer, db.ForeignKey('students.admission_number'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    course_title = db.Column(db.String(255), nullable=False)
    grade = db.Column(db.String(5), nullable=False)

    # Define a relationship with the Student model
    student = db.relationship('Student', backref=db.backref('grades', lazy=True))

    # Define a relationship with the Course model
    course = db.relationship('Course', backref=db.backref('grades', lazy=True))

    # Constructor to initialize Grade Object with attributes.
    def __init__(self, student_admission_number, course_id, course_title, grade, transcript=None):
        self.student_admission_number = student_admission_number
        self.course_id = course_id
        self.course_title = course_title
        self.grade = grade