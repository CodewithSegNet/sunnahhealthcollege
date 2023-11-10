#!/usr/bin/env pyhton3

# Imports
from app.app import db
from werkzeug.security import generate_password_hash, check_password_hash


class Administrator(db.Model):
    '''
    A class that defines the Administrator Description
    '''
    __tablename__ = 'administrators'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    
    # Define a relationship with the Role model
    role = db.relationship('Role', backref=db.backref('administrators', lazy=True))

    # Constructor to initialize Administrator Object with attributes.
    def __init__(self, username, password, role_id):
        self.username = username
        self.password_hash = generate_password_hash(password, method='sha256')
        self.role_id = role_id

    # Check if the entered password matches the stored hashed password
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
