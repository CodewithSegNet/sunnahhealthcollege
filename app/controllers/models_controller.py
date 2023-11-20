#!/usr/bin/env python3


# Import
from flask import Blueprint, request, session, jsonify
from app.app import create_app, db
from app.app.models.student_model import Student


# create a blueprint for user related routes
user_bp = Blueprint('user', __name__)


# create a app instance
app = create_app()



# route to get student by name or admission 
@user_bp.route('/student/<identifier>', methods=['GET'])
def get_student_info(identifier):
    '''
    A function that retrieves a student information
    '''
    # Check if the identifier matches admission number criteria
    if len(identifier) <= 20 and identifier.isdigit():
        student = Student.query.filter_by(admission_number=identifier).first()
    else:
        # Assuming name is longer than 20 charaters
        student = Student.query.filter_by(name=identifier).first()


    if student:
        # Student model has attributes: admission_number, name, date_of_birth, etc.
        student_info = {
            'admission_number': student.admission_number,
            'name': student.name,
            'date_of_birth': student.date_of_birth.strftime('%Y-%m-%d'),
            'department_level': student.department_level,
            'email': student.email,
            'phone_number': student.phone_number,
            'created_at': student.created_at,
            'updated_at': student.updated_at
        }
        return jsonify(student_info), 200
    else:
        return jsonify({'message': 'Student Not Found'}), 400

