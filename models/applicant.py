#!/usr/bin/env python3

# Import
from app import db
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash


class Applicant(db.Model):
    '''
    A class that defines the Applicant Credentials
    '''
    __tablename__ = 'applicants'
    email = db.Column(db.String(255), primary_key=True, unique=True, nullable=False)
    phonenumber = db.Column(db.String(11), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationship with Admission form
    applicant_number = db.relationship('AdmissionForm', backref='applicants')
    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)