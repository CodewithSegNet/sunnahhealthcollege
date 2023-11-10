#!/usr/bin/env python3
from app.app import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship



class StudentAnnouncement(db.Model):
    '''
    A class that defines the StudentAnnouncement Description
    '''
    __tablename__ = 'student_announcements'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    announcement_id = db.Column(db.Integer, db.ForeignKey('announcements.id'), nullable=False)
    admission_number = db.Column(db.Integer, db.ForeignKey('students.admission_number'), nullable=False)
    read_status = db.Column(db.Boolean, default=False, nullable=False)
    
    # Define relationships with the Announcement and Student models
    announcement = db.relationship('Announcement', backref=db.backref('student_announcements', lazy=True))
    student = db.relationship('Student', backref=db.backref('student_announcements', lazy=True))
