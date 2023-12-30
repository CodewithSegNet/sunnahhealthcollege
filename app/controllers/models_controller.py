#!/usr/bin/env python3

# Import
from flask import Blueprint, request, jsonify, session, redirect, url_for
from app.models.student_model import Student
from app.models.department_model import Department
from app.models.semester import Semester
from app.models.course_model import Course
from app.app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import SQLAlchemyError



# create a blueprint for user related routes
user_bp = Blueprint('user', __name__)


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
            'department_name': student.department_name,
            'state': student.state,
            'gender': student.gender,
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
    
    try:
        data = request.json
        existing_student = Student.query.filter_by(admission_number=data['admission_number']).first()
        existing_email = Student.query.filter_by(email=data['email']).first()

        if existing_student:
            return jsonify({'error': 'Admission Number Already Exists!'}), 400
        if existing_email:
            return jsonify({'error': 'Email Already Exists!'}), 400
        





        # Create a new user instance
        new_user = Student(
            admission_number=data['admission_number'],
            password=generate_password_hash(data['password']),
            name=data['name'],
            date_of_birth=data['date_of_birth'],
            department_name = data['department_name'],
            state=data['state'],
            gender=data['gender'],
            email=data['email'],
            phone_number=data['phone_number'],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        db.session.add(new_user)
        db.session.commit()


        
        department_level = 100 
        department_name = 'Pharmacy Technician'


        department = Department.query.filter_by(department_level=department_level).first()
        if department is None:
            # If department doesn't exist, create a new department
            new_department = Department(department_level=department_level, department_name=department_name)
            new_user.departments.append(new_department)
            db.session.add(new_department)            
            db.session.commit()  # Commit changes after creating a new department
        else:
             # If department exists, associate it with the new user
            new_user.departments.append(department)

        if department:
            # Set student_id in department to associate it with the new user
            department.student_id = new_user.admission_number
            db.session.commit()


        # Check if the provided semester exists in the semesters table
        semester_name = data.get('semester')
        if semester_name:
            semester = Semester.query.filter_by(semester=semester_name).first()
            if semester is None:
                new_semester = Semester(semester=semester_name)
                new_user.semesters.append(new_semester)
                db.session.add(new_semester)
                db.session.commit()  # Commit changes after creating a new semester
            else:
                new_user.semesters.append(semester)

            if semester:
            # Set student_id in department to associate it with the new user
                semester.student_id = new_user.admission_number
                db.session.commit() 
        else:
            return jsonify({'error': 'Semester value is missing or invalid'}), 400

        # Add specific courses for the department and department level to the new user
        if department_name == 'Pharmacy Technician' and department_level == 100:
            course1 = Course(course_title='Anatomy and Physiology 1', course_code='GNP 111', credit=3)
            course2 = Course(course_title='General and Physical Chemistry', course_code='BCH 111', credit=3)
            course3 = Course(course_title='Algebra and Elementary Trigonometry', course_code='MTH 112', credit=3)
            course4 = Course(course_title='Supervised Pharmacy practice', course_code='PCT 112', credit=6)
            course5 = Course(course_title='Pharmacology 1', course_code='PCT 111', credit=3)
            course6 = Course(course_title='Use of English', course_code='GNS 101', credit=3)
            course7 = Course(course_title='PHC Management',  course_code='CHE 261', credit=3)

            # Add courses to the database session
            db.session.add(course1)
            db.session.add(course2)
            db.session.add(course3)
            db.session.add(course4)
            db.session.add(course5)
            db.session.add(course6)
            db.session.add(course7)

            # Assign the courses to the new user
            new_user.courses.extend([course1, course2, course3, course4, course5, course6, course7])

        # Add new user to the Database

        
        
        # Add new user to the Database
        db.session.add(new_department)
        db.session.add(new_semester)
        db.session.commit()

        # Return JSON successful message if data's works
        return jsonify({'message': 'User Registration Successfully Created!'}), 201
    
    # Handles database issues (connection or constraint violation)
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    





    
@user_bp.route('/update', methods=['POST', 'PUT'])
def update_course():
    # Assuming you receive data for the course update in the request
    data = request.get_json()

    # Check if data is None or not present
    if data is None:
        return jsonify({'error': 'No data received'}), 400

    # Extract the necessary data for the course update
    course_title = data.get('course_title')
    course_code = data.get('course_code')
    credit = data.get('credit')

    # Check if the required data is present
    if course_title is None or course_code is None or credit is None:
        return jsonify({'error': 'Incomplete data provided'}), 400

    # Assuming there's a Course instance to update (retrieve it based on an identifier)
    course_to_update = Course.query.filter_by(course_code=course_code).first()

    if course_to_update:
        try:
            # Update the course details
            course_to_update.course_title = course_title
            course_to_update.credit = credit

            # Commit the changes to the database
            db.session.commit()

            return jsonify({'message': 'Course updated successfully'}), 200

        except Exception as e:
            db.session.rollback()  # Rollback changes in case of an error
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Course not found'}), 404






@user_bp.route('/update_profile', methods=['POST'])
def update_profile():
    if request.method == 'POST':
        # Retrieve form data
        name = request.form.get('name')
        password = request.form.get('password')
        date_of_birth = request.form.get('date_of_birth')
        gender = request.form.get('gender')
        department_name = request.form.get('department_name')
        email = request.form.get('email')
        state = request.form.get('state')
        phone_number = request.form.get('phone_number')

         # Hash the password before saving
        hashed_password = generate_password_hash(password)
        
        # Fetch the current user from the session
        current_user = Student.query.get(session.get('user_id'))

        # Update user profile data
        current_user.name = name
        current_user.password = hashed_password
        current_user.date_of_birth = date_of_birth
        current_user.gender = gender
        current_user.department_name = department_name
        current_user.email = email
        current_user.state = state
        current_user.phone_number = phone_number

        # Commit changes to the database
        db.session.commit()

        return redirect(url_for('pages.dashboard')) 
    else:
        return jsonify({'error': 'Invalid request method'}), 405



@user_bp.route('/upload_department', methods=['POST'])
def upload_department():
    # Fetch data from the form
    department_level = request.form.get('department_level')
    department_name = request.form.get('department_name')

    # Check if the required data is present
    if not department_level or not department_name:
        return jsonify({'error': 'Incomplete data provided'}), 400

    # Create a new Department instance
    new_department = Department(department_level=department_level, department_name=department_name)

    try:
        # Add the new_department instance to the session
        db.session.add(new_department)

        # Commit the changes to the database
        db.session.commit()

        return jsonify({'message': 'Department added successfully'}), 200

    except Exception as e:
        db.session.rollback()  # Rollback changes in case of an error
        return jsonify({'error': str(e)}), 500


@user_bp.route('/upload_semester', methods=['POST'])
def upload_semester():
    # Fetch data from the form
    semester_name = request.form.get('semester')

    # Check if the required data is present
    if not semester_name:
        return jsonify({'error': 'Incomplete data provided'}), 400

    # Create a new Semester instance
    new_semester = Semester(semester=semester_name)

    try:
        # Add the new_semester instance to the session
        db.session.add(new_semester)

        # Commit the changes to the database
        db.session.commit()

        return jsonify({'message': 'Semester added successfully'}), 200

    except Exception as e:
        db.session.rollback()  # Rollback changes in case of an error
        return jsonify({'error': str(e)}), 500