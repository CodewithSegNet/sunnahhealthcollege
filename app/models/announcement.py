#!/usr/bin/env python3

# Import
from flask_sqlalchemy import SQLAlchemy
from app.app import db
from datetime import datetime
from sqlalchemy import ForeignKey
import re
from sqlalchemy import UniqueConstraint



class Announcement(db.Model):
    '''
    A class that defines the Announcement
    '''
    __tablename__ = 'annoucements'
    announcement_id = db.Column(db.Integer, primary_key=True, nullable=True)
    admin_id = db.Column(db.Integer, db.foreignKey('administrators.admin_id'), nullable=False)
    title = db.Column(db.String, nullable=False)
    message = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False) 
