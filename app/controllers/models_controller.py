#!/usr/bin/env python3

# Import
from datetime import datetime
from app.app import create_app, db
from flask import Blueprint, request, jsonify, session
from sqlalchemy.exc import SQLAlchemyError
from app.models.student_model import Student
from app.models.department_model import Department



# create a blueprint for user related routes
user_bp = Blueprint('user', __name__)


# create a app instance
app = create_app()



# route to get student by name or admission 
@user_bp.route('/student/<path:identifier>', methods=['GET'])
def get_student_info(identifier):
    '''
    A function that retrieves a student information
    '''
    student = None

    print("Identifier:", identifier)

    # Check if the identifier matches admission number criteria
    if identifier:
        student = Student.query.filter_by(admission_number=identifier).first()
    else:
        # Assuming name is longer than 20 characters
        student = Student.query.filter(Student.name.ilike("%{}%".format(identifier))).first()


    if student:
        # Student model has attributes: admission_number, name, date_of_birth, etc.
        print("Retrieved Admission Number:", student.admission_number)


        student_info = {
            'admission_number': student.admission_number,
            'name': student.name,
            'date_of_birth': student.date_of_birth.strftime('%Y-%m-%d'),
            'department_level': student.department_level,
            'department_name': student.department_name,
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
    existing_student = Student.query.filter_by(admission_number = data['admission_number']).first()
    existing_email = Student.query.filter_by(email = data['email']).first()

    if existing_student:
        return jsonify({'error': 'Admission Number Aready Exist!'}), 400
    if existing_email:
        return jsonify({'error': 'Email Already Exist!'}), 400


    try:
        # extract registration data from json
        new_user = Student(
            admission_number = data['admission_number'],
            password = data['password'],
            name = data['name'],
            date_of_birth = data['date_of_birth'],
            department_level = data['department_level'],
            department_name = data['department_name'],
            email = data['email'],
            phone_number = data['phone_number'],
            created_at = datetime.utcnow(),
            updated_at = datetime.utcnow()
        )

       # Check if the provided department_level exists in the departments table
        department_level = data.get('department_level')
        department_name = data.get('department_name')

        department = Department.query.filter_by(department_level=department_level).first()
        if department is None:
            # If department doesn't exist, create a new department
            new_department = Department(department_level=department_level, department_name=department_name)
            db.session.add(new_department)
            db.session.flush()

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