#!/usr/bin/env python3

# Import
from datetime import datetime
from app.app import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship



class Announcement(db.Model):
    '''
    A class that defines the Announcement
    '''
    __tablename__ = 'annoucements'
    announcement_id = db.Column(db.Integer, primary_key=True, nullable=True)
    admin_id = db.Column(db.Integer, db.foreignKey('administrators.announcement_id'), nullable=False)
    title = db.Column(db.String, nullable=False)
    message = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False) 



    # Define a relationship with the Administrator model
    administrator = db.relationship('Administrator', backref=db.backref('announcements', lazy=True))