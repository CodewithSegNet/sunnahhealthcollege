#!/usr/bin/env python3

# Import
from datetime import datetime
from app.app import db
from app.models.administrator_model import Administrator
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship



class Announcement(db.Model):
    '''
    A class that defines the Announcement
    '''
    __tablename__ = 'announcements'
    announcement_id = db.Column(db.Integer, primary_key=True, nullable=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('administrators.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Define a relationship with the Administrator model
    administrator = db.relationship('Administrator', backref=db.backref('announcements', lazy=True))