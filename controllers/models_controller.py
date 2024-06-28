#!/usr/bin/env python3

# Import
from flask import Blueprint, request, jsonify, session, redirect, url_for, render_template
from models import Student, Department, Semester, ContactMessage, Course, Applicant, Specialadmin
from models import Department
from models import Semester
from models import Course
from models import Admin
from models import Applicant
from models import Image
from models import Specialadmin
import json
from app import db
from datetime import datetime
from urllib.parse import quote, unquote
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import SQLAlchemyError



# create a blueprint for user related routes
user_bp = Blueprint('user', __name__)


# /****************************************** COURSES ************************************************/


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
        
        if department_name == 'Pharmacy Technician' and department_level == 300 and semester_name == "first":
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
        if department_name == 'Pharmacy Technician' and department_level == 300 and semester_name == "second":
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
        
        if department_name == 'Community Health Extention' and department_level == 300 and semester_name == "first":
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


    
        # Community Health Extention 300 second semester
        if department_name == 'Community Health Extention' and department_level == 300 and semester_name == "second":
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


# /****************************************** END OF COURSES ************************************************/






# /****************************************** STUDENTS ROUTES ************************************************/


def add_courses_to_user(user, courses_data):
    # Create and assign courses to the new user
    for course_data in courses_data:
        new_course = Course(
            course_code=course_data['course_code'],
            student_id=user.admission_number,
            course_title=course_data['course_title'],
            credit=course_data['credit'],
            ca_score=None,
            exam_score=None,
            total_score=None,
            grade=None,
            remark=None
        )
        db.session.add(new_course)
        user.courses.append(new_course)
            


# route to get student by name or admission 
@user_bp.route('/student', methods=['GET'])
def get_student_info():
    '''
    A function that retrieves a student information
    '''

    identifier = request.args.get('identifier')

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
            'date_of_birth': student.date_of_birth.strftime('%Y-%m-%d') if student.date_of_birth else None,
            'department_name': student.department_name,
            'state': student.state,
            'gender': student.gender,
            'email': student.email,
            'phone_number': student.phone_number,
        }

        # Accessing related objects
        if student.departments:
            student_info['department'] = {
                'department_level': student.departments[0].department_level,
                'department_name': student.departments[0].department_name,
            }

        if student.images:
                latest_image = Image.query.filter_by(student_admission_number=student.admission_number).order_by(Image.created_at.desc()).first()
                if latest_image:
                    student_info['images'] = [
                        {
                            'image_path': latest_image.image_data,
                            'mimetype': 'image/jpeg'
                        }
                    ]
                else:
                    student_info['images'] = []

        if student.courses:
            student_info['courses'] = [
                {
                    'course_code': course.course_code,
                    'course_title': course.course_title,
                    'credit': course.credit,
                    'ca_score': course.ca_score,
                    'exam_score': course.exam_score,
                    'total_score': course.total_score,
                    'grade': course.grade,
                    'remark': course.remark,
                        }
                        for course in student.courses

                    ]
                
            
        if student.semesters:
            student_info['semesters'] = [
                {
                    'semester': semester.semester
                }
                for semester in student.semesters
            ]

        encoded_student_info = quote(json.dumps(student_info))

        return redirect(url_for('pages.admindash', student_info=encoded_student_info))
    else:
        return jsonify({'message': 'Student Not Found'}), 404
    


# /****************************************** END OF STUDENTS ************************************************/




# /****************************************** ADMINS ROUTES ************************************************/


@user_bp.route('/adminregister', methods=['POST'])
def register():
    '''
    A function that handles admin registration
    '''
    
    try:
        data = request.json
        existing_email = Student.query.filter_by(email=data['email']).first()

        if existing_email:
            return jsonify({'error': 'Email Already Exists!'}), 400
        


        # Create a new user instance
        new_user = Admin(
            email=data['email'],
            password=generate_password_hash(data['password']),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        db.session.add(new_user)
        db.session.commit()


        # Return JSON successful message if data's works
        return jsonify({'message': 'Admin Registration Successfully Created!'}), 201
    
    # Handles database issues (connection or constraint violation)
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    


    
@user_bp.route('/specialadminreg', methods=['POST'])
def specialadminreg():
    '''
    A function that handles admin registration
    '''
    
    try:
        data = request.json
        existing_email = Specialadmin.query.filter_by(email=data['email']).first()

        if existing_email:
            return jsonify({'error': 'Email Already Exists!'}), 400
        


        # Create a new user instance
        new_user = Specialadmin(
            email=data['email'],
            password=generate_password_hash(data['password']),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        db.session.add(new_user)
        db.session.commit()


        # Return JSON successful message if data's works
        return jsonify({'message': 'Admin Registration Successfully Created!'}), 201
    
    # Handles database issues (connection or constraint violation)
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500




# /****************************************** END OF ADMINS ROUTES ************************************************/





# /****************************************** REGISTERS ROUTES ************************************************/


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
            department_name = data['department_name'],
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
            semester = Semester.query.filter_by(id=id).first()
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
        

        for course in new_user.courses:
                course.student_id = new_user.admission_number
        
        assign_courses(new_user, department_name, department_level, semester_name)


        db.session.commit()


        # Return JSON successful message if data's works
        return jsonify({'message': 'User Registration Successfully Created!'}), 201
    
    # Handles database issues (connection or constraint violation)
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    



# /****************************************** ENDS OF REGISTERS ROUTES ************************************************/







# /****************************************** UPDATES ROUTES ************************************************/



@user_bp.route('/update_profile', methods=['POST'])
def update_profile():
    if request.method == 'POST':
        # Retrieve form data
        name = request.form.get('name')
        password = request.form.get('password')
        date_of_birth = request.form.get('date_of_birth')
        gender = request.form.get('gender')
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
        current_user.email = email
        current_user.state = state
        current_user.phone_number = phone_number

        # Commit changes to the database
        db.session.commit()

        return redirect(url_for('pages.dashboard')) 
    else:
        return jsonify({'error': 'Invalid request method'}), 405




# Create a route for updating the password using both PUT and POST methods
@user_bp.route('/update_password', methods=['PUT', 'POST'])
def update_password():
    if request.method == 'POST' or request.form.get('_method') == 'PUT':
        admission_number = request.form.get('admission_number')
        new_password = request.form.get('new_password')

        if not new_password:
            return jsonify({'message': 'New password is required'}), 400

        # Get the current student based on admission_number
        student = Student.query.get(admission_number)

        if not student:
            return jsonify({'message': 'Student not found'}), 404

        # Hash the new password before storing it
        hashed_password = generate_password_hash(new_password, method='sha256')
        student.password = hashed_password

        # Update the 'updated_at' timestamp
        student.updated_at = datetime.utcnow()

        # Commit changes to the database
        db.session.commit()

        return redirect(url_for('pages.admindash'))

    else:
        return jsonify({'message': 'Method not allowed'}), 405



# /****************************************** END OF UPDATES ROUTES ************************************************/






