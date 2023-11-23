#!/usr/bin/env python3


# Import
from datetime import datetime
from app.app import create_app, db
from flask import Blueprint, request, jsonify, session
from sqlalchemy.exc import SQLAlchemyError
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
        return jsonify({'message': 'Student Not Found'}), 404
    


@user_bp.route('/register', methods=['POST'])
def registration():
    '''
    A function that handles users registration
    '''


    #
    data = request.json
    existing_student = Student.query.filter_by(admission_number = data['admission_number'])
    existing_email = Student.query.filter_by(email = data['email'])

    if existing_student:
        return jsonify({'error': 'Admission Number Aready Exist!'}), 400
    if existing_email:
        return jsonify({'error': 'Email Already Exist!'}), 400


    try:
        # extract registration data from json
        new_user = Student(
            admission_number = data['admission_number'],
            name = data['name'],
            date_of_birth = data['date_of_birth'],
            department_level = data['department_level'],
            email = data['email'],
            phone_number = data['phone_number'],
            created_at = datetime.utcnow(),
            update_at = datetime.utcnow(),
        )

        try:
            new_user.validate_email(data['email'])
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        
        # add New User to the Database
        db.session.add(new_user)
        db.session.commit()

        # return JSON successful message if data's works
        return jsonify({'message': 'User Registration Successfully Created!'}), 201
    
    # handles database issues(connection or constraint violation)
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

    
                

