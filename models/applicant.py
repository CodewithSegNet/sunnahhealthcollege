#!/usr/bin/env python3

# Import
from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class Applicant(db.Model):
    email = db.Column(db.String(255), primary_key=True, unique=True, nullable=False)
    phonenumber = db.Column(db.String(11), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
  


    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)