#!/usr/bin/env python3

# Import
from app import db
from models.department_model import Department
import models.student_model
from models.semester import Semester
from datetime import datetime
from sqlalchemy.orm import relationship





class FormImage(db.Model):
    __tablename__ = 'photograph'
    id = db.Column(db.Integer, primary_key=True)
    form_id = db.Column(db.Integer, db.ForeignKey('admissionforms.id'), nullable=False)
    image_data = db.Column(db.LargeBinary(length=4294967295)) 
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
