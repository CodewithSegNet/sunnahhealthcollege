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
    



def assign_courses(user, department_name, department_level, semester_name):
    
        # Add specific courses for the department and department level to the new user
        if department_name == 'Pharmacy Technician' and department_level == 100 and semester_name == "first":
            course1 = Course(course_title='Anatomy and Physiology 1', course_code='GNP 111', credit=3)
            course2 = Course(course_title='General and Physical Chemistry', course_code='BCH 111', credit=3)
            course3 = Course(course_title='Algebra and Elementary Trigonometry', course_code='MTH 112', credit=3)
            course4 = Course(course_title='Supervised Pharmacy practice', course_code='PCT 112', credit=6)
            course5 = Course(course_title='Pharmacology 1', course_code='PCT 111', credit=3)
            course6 = Course(course_title='Use of English', course_code='GNS 101', credit=3)
            course7 = Course(course_title='PHC Management',  course_code='CHE 261', credit=3)
  
  
            # Add courses to the database session
            db.session.add_all([course1, course2, course3, course4, course5, course6, course7])

            # Assign the courses to the new user
            user.courses.extend([course1, course2, course3, course4, course5, course6, course7])
        

        #  Add specific courses for the department and department level to the new user
        if department_name == 'Pharmacy Technician' and department_level == 100 and semester_name == "second":
            course1 = Course(course_title='Mechanics and Properties of matter and Heart Energy', course_code='BPH 111', credit=3)
            course2 = Course(course_title='Anatomy and Physiology II', course_code='GNP 121', credit=3)
            course3 = Course(course_title='Intro to Computer', course_code='COM 111', credit=3)
            course4 = Course(course_title='General Laboratory', course_code='GLT 111', credit=3)
            course5 = Course(course_title='Intro to dispensing theory and practical', course_code='PCT 121', credit=3)
            course6 = Course(course_title='Communication in English', course_code='GNS 102', credit=3)
            course7 = Course(course_title='Supervised Pharmacy Practice',  course_code='PCT 122', credit=6)
  
  
            # Add courses to the database session
            db.session.add_all([course1, course2, course3, course4, course5, course6, course7])

            # Assign the courses to the new user
            user.courses.extend([course1, course2, course3, course4, course5, course6, course7, course8, course9])
        
        
        
        
        
        # Pharmacy Technician 200 first semester
        
        if department_name == 'Pharmacy Technician' and department_level == 200 and semester_name == "first":
            course1 = Course(course_title='Dispensing theory 1', course_code='PCT 122', credit=2)
            course2 = Course(course_title='Dispensing practical 1', course_code='PCT 212', credit=4)
            course3 = Course(course_title='Intro to Drug & Quality Assurance', course_code='PCT 213', credit=2)
            course4 = Course(course_title='Supervised Pharmacy Practice', course_code='PCT 214', credit=6)
            course5 = Course(course_title='Statistics', course_code='STA 111', credit=2)
            course6 = Course(course_title='Organic and Inorganic Chemistry', course_code='BCH 121', credit=3)
            course7 = Course(course_title='Sources of Water and Sanitation',  course_code='EHT 123', credit=2)
            course8 = Course(course_title='Technical Drawing',  course_code='PTD 111', credit=3)
            course9 = Course(course_title='Introduction to Microbology',  course_code='STB 111', credit=3)



            # Add courses to the database session
            db.session.add_all([course1, course2, course3, course4, course5, course6, course7, course8, course9])


            # Assign the courses to the new user
            user.courses.extend([course1, course2, course3, course4, course5, course6, course7, course8, course9])


    
        # Pharmacy Technician 200 second semester
        if department_name == 'Pharmacy Technician' and department_level == 200 and semester_name == "second":
            course1 = Course(course_title='Dispensing theory II', course_code='PCT 221', credit=3)
            course2 = Course(course_title='Dispensing practical II', course_code='PCT 222', credit=2)
            course3 = Course(course_title='Supervised Pharmacy Practice', course_code='PCT 223', credit=6)
            course4 = Course(course_title='Principle of pharmacy Technician practice', course_code='PCT 224', credit=2)
            course5 = Course(course_title='Pharmacology II', course_code='GNP 214', credit=2)
            course6 = Course(course_title='Drugs Revolving Fund', course_code='CHE 256', credit=2)
            course7 = Course(course_title='Food and Nutrition',  course_code='FST 215', credit=3)



            # Add courses to the database session
            db.session.add_all([course1, course2, course3, course4, course5, course6, course7])


            # Assign the courses to the new user
            user.courses.extend([course1, course2, course3, course4, course5, course6, course7])


                
        # Pharmacy Technician 300 first semester
        
        if department_name == 'Pharmacy Technician' and department_level == 200 and semester_name == "first":
            course1 = Course(course_title='Research Methodology', course_code='GNS 228', credit=6)
            course2 = Course(course_title='Family Planning and Reproductive Health', course_code='GNP 221', credit=3)
            course3 = Course(course_title='Citizenship', course_code='GNS 111', credit=3)
            course4 = Course(course_title='Pharmacy Laws and Ethics', course_code='PCT 312', credit=2)
            course5 = Course(course_title='Supervised Pharmacy Practice', course_code='PCT 313', credit=6)
            course6 = Course(course_title='Actions and Uses of Common Medicine', course_code='PCT 314', credit=4)



            # Add courses to the database session
            db.session.add_all([course1, course2, course3, course4, course5, course6])


            # Assign the courses to the new user
            user.courses.extend([course1, course2, course3, course4, course5, course6])


    
        # Pharmacy Technician 300 second semester
        if department_name == 'Pharmacy Technician' and department_level == 200 and semester_name == "second":
            course1 = Course(course_title='Intro to Medical Sociolgy', course_code='GNS 213', credit=2)
            course2 = Course(course_title='Entrepreneurship', course_code='BUS 213', credit=2)
            course3 = Course(course_title='Research/Project Writing', course_code='CHE 265', credit=6)
            course4 = Course(course_title='Seminar', course_code='PCT 311', credit=3)



            # Add courses to the database session
            db.session.add_all([course1, course2, course3, course4])


            # Assign the courses to the new user
            user.courses.extend([course1, course2, course3, course4])





             # Add specific courses for the department Community Health Extention
        if department_name == 'Community Health Extention' and department_level == 100 and semester_name == "first":
            course1 = Course(course_title='Use of English', course_code='GNS 101', credit=2)
            course2 = Course(course_title='Professional Ethics', course_code='CHE 211', credit=1)
            course3 = Course(course_title='Anatomy and Physiology I', course_code='CHE 212', credit=2)
            course4 = Course(course_title='Behaviour Change Communications', course_code='CHE 213', credit=2)
            course5 = Course(course_title='Citizenship Education', course_code='GNS 111', credit=1)
            course6 = Course(course_title='Human Nutrition', course_code='CHE 214', credit=2)
            course7 = Course(course_title='Intro to Primary Health Care',  course_code='CHE 215', credit=2)
            course8 = Course(course_title='Intro to Psychology',  course_code='GNS 411', credit=1)
            course9 = Course(course_title='Intro to Environmental Health',  course_code='EHT 111', credit=2)
            course10 = Course(course_title='Geography',  course_code='FOT 111', credit=1)
            course11 = Course(course_title='Intro to Computer',  course_code='COM 111', credit=2)
            course12 = Course(course_title='Intro to Medical Sociology',  course_code='GNS 213', credit=2)

  
            # Add courses to the database session
            db.session.add_all([course1, course2, course3, course4, course5, course6, course7, course8, course9, course10, course11, course12])

            # Assign the courses to the new user
            user.courses.extend([course1, course2, course3, course4, course5, course6, course7, course8, course9, course10, course11, course12])
        

        #  Add specific courses for the department and department level to the new user
        if department_name == 'Community Health Extention' and department_level == 100 and semester_name == "second":
            course1 = Course(course_title='Symptomatology', course_code='CHE 221', credit=2)
            course2 = Course(course_title='Population Dynamics and Family Planning', course_code='CHE 222', credit=3)
            course3 = Course(course_title='Clinical Skills I', course_code='CHE 223', credit=3)
            course4 = Course(course_title='Science Laboratory Technology', course_code='STB 211', credit=3)
            course5 = Course(course_title='Immunity and Immunization', course_code='CHE 224', credit=2)
            course6 = Course(course_title='Control of Communicable Diseases', course_code='CHE 225', credit=2)
            course7 = Course(course_title='Accident and Emergency',  course_code='CHE 226', credit=2)
            course8 = Course(course_title='Supervised Clinical Experience I',  course_code='CHE 227', credit=3)
            course9 = Course(course_title='Communication in English',  course_code='GNS 102', credit=2)

  
            # Add courses to the database session
            db.session.add_all([course1, course2, course3, course4, course5, course6, course7, course8, course9])

            # Assign the courses to the new user
            user.courses.extend([course1, course2, course3, course4, course5, course6, course7, course8, course9])
        
        
        
        
        
        # Community Health Extention 200 first semester
        
        if department_name == 'Community Health Extention' and department_level == 200 and semester_name == "first":
            course1 = Course(course_title='Anatomy and Physiolology II', course_code='CHE 231', credit=2)
            course2 = Course(course_title='Oral Health', course_code='CHE 232', credit=2)
            course3 = Course(course_title='Community Mental Health', course_code='CHE 233', credit=2)
            course4 = Course(course_title='Reproductive Health', course_code='CHE 234', credit=2)
            course5 = Course(course_title='Child Health', course_code='CHE 235', credit=3)
            course6 = Course(course_title='School Health Programme', course_code='CHE 236', credit=2)
            course7 = Course(course_title='Control of Non-Communicable Disease',  course_code='CHE 237', credit=2)
            course8 = Course(course_title='Intro to Physical Chemistry',  course_code='BCH 111', credit=1)
            course9 = Course(course_title='Community linkage and Development',  course_code='CHE 238', credit=3)
            course10 = Course(course_title='Care and Management of HIV and AIDS',  course_code='CHE 239', credit=2)
            course11 = Course(course_title='Occupational Health and Safety',  course_code='CHE 240', credit=2)



            # Add courses to the database session
            db.session.add_all([course1, course2, course3, course4, course5, course6, course7, course8, course9, course10, course11])


            # Assign the courses to the new user
            user.courses.extend([course1, course2, course3, course4, course5, course6, course7, course8, course9, course10, course11])


    
        # Community Health Extention 200 second semester
        if department_name == 'Community Health Extention' and department_level == 200 and semester_name == "second":
            course1 = Course(course_title='Clinical Skills II', course_code='CHE 241', credit=3)
            course2 = Course(course_title='Maternal Health', course_code='CHE 242', credit=4)
            course3 = Course(course_title='Modified Essential Newborn Care', course_code='CHE 243', credit=3)
            course4 = Course(course_title='Community Ear Nose and Throat Care(ENT)', course_code='CHE 244', credit=2)
            course5 = Course(course_title='Community Eye Care', course_code='CHE 245', credit=1)
            course6 = Course(course_title='Use of Standing Orders', course_code='CHE 246', credit=3)
            course7 = Course(course_title='Intro to Pharmacology',  course_code='GNP 123', credit=2)
            course8 = Course(course_title='Nigerian Health System',  course_code='CHE 247', credit=2)
            course9 = Course(course_title='Supervised Clinical Experience II',  course_code='CHE 248', credit=4)



            # Add courses to the database session
            db.session.add_all([course1, course2, course3, course4, course5, course6, course7, course8, course9])


            # Assign the courses to the new user
            user.courses.extend([course1, course2, course3, course4, course5, course6, course7, course8, course9])


                
        # Community Health Extention 300 first semester
        
        if department_name == 'Community Health Extention' and department_level == 200 and semester_name == "first":
            course1 = Course(course_title='Care of the Older Persons', course_code='CHE 251', credit=1)
            course2 = Course(course_title='Care of Persons with Special Needs', course_code='CHE 252', credit=2)
            course3 = Course(course_title='Health Statistics', course_code='CHE 253', credit=2)
            course4 = Course(course_title='Essential Medicines', course_code='CHE 254', credit=2)
            course5 = Course(course_title='Human Resource for Health', course_code='CHE 255', credit=1)
            course6 = Course(course_title='Research Methodology', course_code='CHE 256', credit=2)
            course7 = Course(course_title='Community Based Newborn Care', course_code='CHE 257', credit=2)
            course8 = Course(course_title='Supervised Community Based Experience(SCBE)', course_code='CHE 258', credit=4)



            # Add courses to the database session
            db.session.add_all([course1, course2, course3, course4, course5, course6, course7, course8])


            # Assign the courses to the new user
            user.courses.extend([course1, course2, course3, course4, course5, course6, course7, course8])


    
        # Pharmacy Technician 300 second semester
        if department_name == 'Community Health Extention' and department_level == 200 and semester_name == "second":
            course1 = Course(course_title='Primary Health Care Management', course_code='CHE 261', credit=2)
            course2 = Course(course_title='Referral System and Outreach services', course_code='CHE 262', credit=2)
            course3 = Course(course_title='Accounting System in Primary Health Care', course_code='CHE 263', credit=2)
            course4 = Course(course_title='Health Management Information System', course_code='CHE 264', credit=2)
            course5 = Course(course_title='Entrepreneurship Education', course_code='BUS 213', credit=6)
            course6 = Course(course_title='Research Project', course_code='CHE 265', credit=3)



            # Add courses to the database session
            db.session.add_all([course1, course2, course3, course4, course5, course6])


            # Assign the courses to the new user
            user.courses.extend([course1, course2, course3, course4, course5, course6])




        # medical Laboratory Technician 100 first semester
        if department_name == 'medical laboratory technician' and department_level == 100 and semester_name == "first":
            course1 = Course(course_title='Communication Skills I', course_code='ELS 101', credit=2)
            course2 = Course(course_title='Introduction to IT I', course_code='CSC 101', credit=2)
            course3 = Course(course_title='General Chemistry', course_code='CHM 101', credit=3)
            course4 = Course(course_title='General Biology I', course_code='BIO 101', credit=3)
            course5 = Course(course_title='General Physics I', course_code='PHY 101', credit=3)
            course6 = Course(course_title='General Mathematics I', course_code='MTH 101', credit=2)
            course7 = Course(course_title='Citizenship Education',  course_code='GST 101', credit=2)
            course8 = Course(course_title='History and Philosophy of Science',  course_code='GST 103', credit=2)
            course9 = Course(course_title='Intro to Environmental Health',  course_code='EHT 101', credit=2)
            course10 = Course(course_title='Functional French I',  course_code='FRN 101', credit=2)


            # Add courses to the database session
            db.session.add_all([course1, course2, course3, course4, course5, course6, course7, course8, course9, course10])


            # Assign the courses to the new user
            user.courses.extend([course1, course2, course3, course4, course5, course6, course7, course8, course9, course10])


        # medical Laboratory Technician 100 second semester
        if department_name == 'medical laboratory technician' and department_level == 100 and semester_name == "second":
            course1 = Course(course_title='Communication Skills II', course_code='ELS 102', credit=2)
            course2 = Course(course_title='Introduction to IT II', course_code='CSC 102', credit=2)
            course3 = Course(course_title='Organic Chemistry', course_code='CHM 102', credit=3)
            course4 = Course(course_title='General Biology II', course_code='BIO 102', credit=3)
            course5 = Course(course_title='General Physics II', course_code='PHY 102', credit=3)
            course6 = Course(course_title='General Mathematics II', course_code='MTH 102', credit=2)
            course7 = Course(course_title='First Aid and Primary Healthcare',  course_code='FAP 102', credit=2)
            course8 = Course(course_title='Philosophy & Logic/Critical Reasoning',  course_code='GST 102', credit=2)
            course9 = Course(course_title='Functional French II',  course_code='FRN 102', credit=2)


            # Add courses to the database session
            db.session.add_all([course1, course2, course3, course4, course5, course6, course7, course8, course9])


            # Assign the courses to the new user
            user.courses.extend([course1, course2, course3, course4, course5, course6, course7, course8, course9])



            
        # medical Laboratory Technician 200 first semester
        if department_name == 'medical laboratory technician' and department_level == 200 and semester_name == "first":
            course1 = Course(course_title='Basic Anatomy', course_code='ANA 201', credit=3)
            course2 = Course(course_title='Basic Physiology', course_code='PHS 201', credit=3)
            course3 = Course(course_title='Basic Biochemistry', course_code='BCH 201', credit=3)
            course4 = Course(course_title='Intro to MLS', course_code='MLT 201', credit=3)
            course5 = Course(course_title='Intro to Immunology', course_code='MLT 203', credit=2)
            course6 = Course(course_title='Clinical Laboratory Posting I', course_code='MLT 205', credit=3)
            course7 = Course(course_title='Basic Laboratory Techniques I',  course_code='MLT 207', credit=2)
            course8 = Course(course_title='Basic Cytology and Genetics',  course_code='BIO 201', credit=2)


            # Add courses to the database session
            db.session.add_all([course1, course2, course3, course4, course5, course6, course7, course8])


            # Assign the courses to the new user
            user.courses.extend([course1, course2, course3, course4, course5, course6, course7, course8])



        # medical Laboratory Technician 200 second semester
        if department_name == 'medical laboratory technician' and department_level == 200 and semester_name == "second":
            course1 = Course(course_title='Medical Microbiology I', course_code='MLT 202', credit=3)
            course2 = Course(course_title='Haematology I', course_code='MLT 204', credit=3)
            course3 = Course(course_title='Research Methodology', course_code='MLT 210', credit=2)
            course4 = Course(course_title='Intro to Management, lab organization & ethics', course_code='MLT 212', credit=2)
            course5 = Course(course_title='Clinical Laboratory Posting II', course_code='MLT 214', credit=3)
            course6 = Course(course_title='Basic Laboratory Techniques II', course_code='MLT 216', credit=2)
            course7 = Course(course_title='Histopathology I',  course_code='MLT 208', credit=3)
            course8 = Course(course_title='Clinical Chemistry',  course_code='MLT 206', credit=3)


            # Add courses to the database session
            db.session.add_all([course1, course2, course3, course4, course5, course6, course7, course8])


            # Assign the courses to the new user
            user.courses.extend([course1, course2, course3, course4, course5, course6, course7, course8])




        # medical Laboratory Technician 300 first semester
        if department_name == 'medical laboratory technician' and department_level == 300 and semester_name == "first":
            course1 = Course(course_title='Medical Parasitology', course_code='MLT 301', credit=3)
            course2 = Course(course_title='Blood Transfusion Science', course_code='MLT 303', credit=3)
            course3 = Course(course_title='Clinical Chemistry II', course_code='MLT 305', credit=3)
            course4 = Course(course_title='Histopathology II', course_code='MLT 307', credit=3)
            course5 = Course(course_title='Seminar in Laboratory Posting III', course_code='MLT 311', credit=3)
            course6 = Course(course_title='Seminar in Laboratory Science', course_code='MLT 309', credit=3)
            course7 = Course(course_title='Introductory Virology',  course_code='MLT 313', credit=2)


            # Add courses to the database session
            db.session.add_all([course1, course2, course3, course4, course5, course6, course7])


            # Assign the courses to the new user
            user.courses.extend([course1, course2, course3, course4, course5, course6, course7])
            
            

        # medical Laboratory Technician 300 Second semester
        if department_name == 'medical laboratory technician' and department_level == 300 and semester_name == "second":
            course1 = Course(course_title='Medical Microbiology II', course_code='MLT 302', credit=3)
            course2 = Course(course_title='Haematology II', course_code='MLT 304', credit=3)
            course3 = Course(course_title='Clinical Chemistry III', course_code='MLT 306', credit=2)
            course4 = Course(course_title='Histopathology III', course_code='MLT 308', credit=2)
            course5 = Course(course_title='Research Project', course_code='MLT 312', credit=6)
            course6 = Course(course_title='Good Laboratory Practice', course_code='MLT 310', credit=2)


            # Add courses to the database session
            db.session.add_all([course1, course2, course3, course4, course5, course6])


            # Assign the courses to the new user
            user.courses.extend([course1, course2, course3, course4, course5, course6])
            










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


        
        department_level = data.get('department_level')
        department_name = data.get('department_name')
        id = 0

        department = Department.query.filter_by(id=id).first()
        if department is None:
            # If department doesn't exist, create a new department
            new_department = Department(department_level=department_level, department_name=department_name)
            new_user.departments.append(new_department)  
            db.session.add(new_department)          
            db.session.commit()  # Commit changes after creating a new department

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
        

        assign_courses(new_user, department_name, department_level, semester_name)



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