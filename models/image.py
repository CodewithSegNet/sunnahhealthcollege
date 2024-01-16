#!/usr/bin/env python3

# Import
from app import db
from models.department_model import Department
import models.student_model
from models.semester import Semester
from datetime import datetime
from sqlalchemy.orm import relationship





class Image(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True)
    student_admission_number = db.Column(db.String(50), db.ForeignKey('students.admission_number'), nullable=False)
    image_data = db.Column(db.LargeBinary(length=1000))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
