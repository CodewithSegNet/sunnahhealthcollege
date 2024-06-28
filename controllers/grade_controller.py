#!/usr/bin/python3

# Import
from models import Course
from models import Department
from models import Image
from app import db
from datetime import datetime
import re
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField, IntegerField
from wtforms.validators import DataRequired

# Define student scores
class StudentScoreForm(FlaskForm):
    ca_score = IntegerField('CA Score', validators=[DataRequired()])
    exam_score = IntegerField('Exam Score', validators=[DataRequired()])
    course_code = StringField('Course code', validators=[DataRequired()])
    student_id = StringField('Student ID', validators=[DataRequired()])
    submit = SubmitField('Add Scores')



