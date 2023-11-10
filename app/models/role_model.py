#!/usr/bin/env python3
from app.app import db

class Role(db.Model):
    '''
    A class that defines the Role Description
    '''
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    role_name = db.Column(db.String(50), unique=True, nullable=False)

    # Constructor to initialize Role Object with attributes.
    def __init__(self, role_name):
        self.role_name = role_name
