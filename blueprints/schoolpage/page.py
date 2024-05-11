#!/usr/bin/env python3
from flask import current_app, Blueprint, render_template, jsonify, request, url_for, session, redirect, send_file, send_from_directory, make_response, flash
from models.student_model import Student
from models.admin import Admin
from controllers.grade_controller import StudentScoreForm
from models.contactmessage import ContactMessage
from models.form import AdmissionForm
from models.special import Specialadmin
from models.image import Image
from models.newsletter import Newsletter
from app import cache, db
from functools import wraps
import traceback
from controllers.models_controller import *
import requests
from urllib.parse import quote, unquote
import jwt
from io import BytesIO
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import os
import pymysql
from MySQLdb import OperationalError
from dotenv import load_dotenv
import time 
import traceback



pages_bp = Blueprint("pages", __name__, template_folder="templates")


# Load environment variables from the .env file
load_dotenv()

@pages_bp.route('/')
@cache.cached(timeout=500)
def home():
    """
    A route that handles the app homepage
    """

    image1 = os.path.join(current_app.config['UPLOAD_FOLDER'], 'section-img.png')
    image2 = os.path.join(current_app.config['UPLOAD_FOLDER'], 'slider.jpg')
    image3 = os.path.join(current_app.config['UPLOAD_FOLDER'], 'student.jpg')
    image4 = os.path.join(current_app.config['UPLOAD_FOLDER'], 'sunnahlogo.jpg')
    image5 = os.path.join(current_app.config['UPLOAD_FOLDER'], 'sunPics1.jpg')
    image6 = os.path.join(current_app.config['UPLOAD_FOLDER'], 'sunPics2.jpg')
    # image7 = os.path.join(app.config['UPLOAD_FOLDER'], 'icon-close.svg')
    return render_template('pages/homepage.html', user_image = image1, user_image2 = image2, user_image3 = image3, user_image4 = image4, user_image5 = image5, user_image6 = image6)



    
@pages_bp.route('/login', methods=['POST'])
def login():
    """
    a route that handles students authentication
    """
    try:
        admission_number = request.form['admission_number']
        password = request.form['password']
        
        user = Student.query.filter_by(admission_number=admission_number).first()
        if user and user.check_password(password):
            """
            create a jwt token
            """
            token = jwt.encode({
                'user_id': user.admission_number,
                'exp': datetime.utcnow() + timedelta(hours=2) # Token expiration Time
            }, 'secret_key', algorithm='HS256')

            session['token'] = token # Store token in the session
            session['user_id'] = user.admission_number # Store user ID in the session

            return redirect(url_for('pages.dashboard'))
        else:
            return redirect(url_for('pages.signinstudent'))    
    except Exception as e:
        return jsonify({'error': "An error occured: {}".format(str(e))})
    


@pages_bp.route('/admin', methods=['POST'])
def admin():
    """
    A route that handles admin authentication
    """
    try:
        email = request.form.get('email')
        password = request.form.get('password')

        if email is None or password is None:
            return jsonify({'error': 'Email and password are required.'}), 400

        user = Admin.query.filter_by(email=email).first()
        if user and user.check_password(password):
            """
            Create a JWT token
            """
            token = jwt.encode({
                'admin_user_id': user.email,
                'exp': datetime.utcnow() + timedelta(hours=2)  # Token expiration time
            }, 'secret_key', algorithm='HS256')

            session['admin_token'] = token  # Store the token in the session
            session['admin_user_id'] = user.email  # Store user ID in the session

            return redirect(url_for('pages.admindash'))
        else:
            return redirect(url_for('pages.signinadmin'))
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500




  # authenticate and authorize requests using JWT
def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            data = jwt.decode(token, 'secret_key', algorithms=['HS256'])
            current_user = Student.query.get(data['user_id'])
        except:
            return jsonify({'error': 'Token is invalid'}), 401
        
        return func(current_user, *args, **kwargs)
    return decorated



# Function to make authorized requests
def make_authorized_request(url, method='GET', data=None, token=None):
    token = token or session.get('token')
    
    if token:
        headers = {'Authorization': f'Bearer {token}'}

        try:
            if method == 'GET':
                response = requests.get(url, headers=headers)
            elif method == 'POST':
                response = requests.post(url, headers=headers, data=data)
            # Add other request methods as needed

            response.raise_for_status()  # Raise an error for 4xx or 5xx status codes
            return response.json() if response.ok else {'error': 'Request failed'}

        except requests.exceptions.RequestException as e:
            return {'error': f'Request failed: {e}'}

    return {'error': 'Token is missing'}


@pages_bp.route('/applicantpage', methods=['POST', 'GET'])
def applicantpage():
    """
    A route that handles applicant authentication
    """
    try:
        email = request.form.get('email')
        password = request.form.get('password')

        if email is None or password is None:
            return jsonify({'error': 'Email and password are required.'}), 400

        user = Applicant.query.filter_by(email=email).first()
        if user and user.check_password(password):
            """
            Create a JWT token
            """
            token = jwt.encode({
                'admin_user_id': user.email,
                'exp': datetime.utcnow() + timedelta(hours=2)  # Token expiration time
            }, 'secret_key', algorithm='HS256')

            session['applicant_token'] = token  # Store the token in the session
            session['applicant_user_id'] = user.email  # Store user ID in the session

            return redirect(url_for('pages.applicantboard'))
        else:
            return redirect(url_for('pages.applicantlogin'))
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500



@pages_bp.route('/signinstudent')
@cache.cached(timeout=500)
def signinstudent():
    """
     A Route thats handles the StudentSignIn
    """

    image1 = os.path.join(current_app.config['UPLOAD_FOLDER'], 'sunnah_college_logo-removebg-preview.png')

    return render_template('pages/signinStudent.html', user_image = image1)



@pages_bp.route('/signinadmin')
@cache.cached(timeout=500)
def signinadmin():

    image1 = os.path.join(current_app.config['UPLOAD_FOLDER'], 'sunnah_college_logo-removebg-preview.png')

    return render_template('pages/signinAdmin.html', user_image = image1)




@pages_bp.route('/contact')
@cache.cached(timeout=500)
def contact():
    """
     A Route thats handles the StudentSignIn
    """

    image1 = os.path.join(current_app.config['UPLOAD_FOLDER'], 'section-img.png')
    image4 = os.path.join(current_app.config['UPLOAD_FOLDER'], 'sunnahlogo.jpg')

    return render_template('pages/contact.html',  user_image = image1, user_image4 = image4)


@pages_bp.route('/admission')
@cache.cached(timeout=500)
def admission():
    """
     A Route thats handles the admission page
    """

    image4 = os.path.join(current_app.config['UPLOAD_FOLDER'], 'sunnahlogo.jpg')

    return render_template('pages/admission.html', user_image4 = image4)






@pages_bp.route('/history')
@cache.cached(timeout=500)
def history():
    """
     A Route thats handles the history page
    """

    image4 = os.path.join(current_app.config['UPLOAD_FOLDER'], 'sunnahlogo.jpg')
    
    return render_template('pages/history.html', user_image4 = image4)




@pages_bp.route('/vision')
@cache.cached(timeout=500)
def vision():
    """
     A Route thats handles the vision page
    """

    image4 = os.path.join(current_app.config['UPLOAD_FOLDER'], 'sunnahlogo.jpg')

    return render_template('pages/vision.html', user_image4 = image4)



@pages_bp.route('/programmes')
@cache.cached(timeout=500)
def programmes():
    """
     A Route thats handles the programmes page
    """

    image4 = os.path.join(current_app.config['UPLOAD_FOLDER'], 'sunnahlogo.jpg')
    
    return render_template('pages/programmes.html', user_image4 = image4)



@pages_bp.route('/application')
@cache.cached(timeout=500)
def application():
    """
     A Route thats handles the application page
    """
    image4 = os.path.join(current_app.config['UPLOAD_FOLDER'], 'sunnahlogo.jpg')
    
    return render_template('pages/application.html', user_image4 = image4)




@pages_bp.route('/form')
@cache.cached(timeout=500)
def form():
    """
     A Route thats handles the application page
    """
    image4 = os.path.join(current_app.config['UPLOAD_FOLDER'], 'sunnahlogo.jpg')
    
    return render_template('pages/application_form.html', user_image = image4)



@pages_bp.route('/notfound')
@cache.cached(timeout=500)
def notfound():
    """
     A Route thats handles the 404 page
    """
    image4 = os.path.join(current_app.config['UPLOAD_FOLDER'], 'sunnahlogo.jpg')

    return render_template('pages/404.html', user_image4 = image4)



@pages_bp.route('/applicant')
@cache.cached(timeout=500)
def applicant():
    """
     A Route thats handles the application page
    """
    image4 = os.path.join(current_app.config['UPLOAD_FOLDER'], 'sunnahlogo.jpg')
    
    return render_template('pages/applicant.html', user_image4 = image4)




@pages_bp.route('/applicantlogin')
@cache.cached(timeout=500)
def applicantlogin():
    """
     A Route thats handles the application page
    """
    image4 = os.path.join(current_app.config['UPLOAD_FOLDER'], 'sunnahlogo.jpg')
    
    return render_template('pages/applicantloginpage.html', user_image4 = image4)





@pages_bp.route('/speciallog')
@cache.cached(timeout=500)
def speciallog():
    """
     A Route thats handles the application page
    """
    image4 = os.path.join(current_app.config['UPLOAD_FOLDER'], 'sunnahlogo.jpg')
    
    return render_template('pages/special.html', user_image4 = image4)



def get_latest_image_info(admission_number):
    if admission_number:
        # Retrieve the latest image associated with the student
        image = Image.query.filter_by(student_admission_number=admission_number).order_by(Image.created_at.desc()).first()

        if image and image.image_data:
            return {
                'image_data': image.image_data,
                'mimetype': 'image/jpeg',  
            }

    return None



@pages_bp.route('/admindash', methods=['GET'])
def admindash():
    if 'admin_user_id' in session:
        email = session.get('admin_user_id')
        token = session.get('admin_token')

        if not email or not token:
            return jsonify({'error': 'Unauthorized'}), 401
    
        user = Admin.query.filter_by(email=email).first()

         # Retrieve student_info from the query parameters
        student_info_param = request.args.get('student_info')

        if student_info_param is None:
            # Handle the case where student_info_param is None
            student_info = None
            image_info = None
        else:
            # Decode the URL-encoded JSON string
            student_info_param_decoded = unquote(student_info_param)

            # Decode again in case of double encoding
            student_info = json.loads(unquote(student_info_param_decoded))

            # Get image information
            image_info = get_latest_image_info(student_info.get('admission_number'))

        image1 = os.path.join(current_app.config['UPLOAD_FOLDER'], 'sunnahlogo.jpg')

        form = StudentScoreForm()

        return render_template('pages/admin.html', user=user, user_image=image1, os=os, student_info=student_info, image_info=image_info, form=form)
    else:
        return jsonify({'error': 'Unauthorized'}), 401







@pages_bp.route('/specialadmin', methods=['POST', 'GET'])
def specialadmin():
    """
    A route that handles applicant authentication
    """
    try:
        email = request.form.get('email')
        password = request.form.get('password')

        if email is None or password is None:
            return jsonify({'error': 'Email and password are required.'}), 400

        user = Specialadmin.query.filter_by(email=email).first()
        if user and user.check_password(password):
            """
            Create a JWT token
            """
            token = jwt.encode({
                'special_user_id': user.email,
                'exp': datetime.utcnow() + timedelta(hours=2)  
            }, 'secret_key', algorithm='HS256')

            session['special_token'] = token  
            session['special_user_id'] = user.email  

            return redirect(url_for('pages.specialadmindashboard'))
        else:
            return redirect(url_for('pages.speciallog'))
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500





@pages_bp.route('/specialadmindashboard', methods=['GET'])
def specialadmindashboard():
    if 'special_user_id' in session:
        email = session.get('special_user_id')
        token = session.get('special_token')

        if not email or not token:
            return jsonify({'error': 'Unauthorized'}), 401
    
        user = Specialadmin.query.filter_by(email=email).first()

        applicants = Applicant.query.options(db.joinedload(Applicant.applicant_number)).all()

        image1 = os.path.join(current_app.config['UPLOAD_FOLDER'], 'sunnahlogo.jpg')

        return render_template('pages/specialdashboard.html', user=user, user_image=image1, applicants=applicants)
    else:
        return jsonify({'error': 'Unauthorized'}), 401









@pages_bp.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        admission_number = session.get('user_id')
        token = session.get('token')

    if not admission_number or not token:
        return jsonify({'error': 'Unauthorized'}), 401
    
    current_user = Student.query.get(admission_number)
    courses = current_user.courses
    departments = current_user.departments  
    semesters = current_user.semesters
    images = current_user.images
   

    # Manually replace slashes with %2F
    encoded_admission_number = current_user.admission_number.replace('/', '%2F')

    user_image_path = f"/images?admission_number={encoded_admission_number}"
      
    
    image1 = os.path.join(current_app.config['UPLOAD_FOLDER'], 'sunnahlogo.jpg')

    return render_template('pages/dashboard.html', student=current_user, departments=departments, semesters=semesters, courses=courses, user_image=image1, user_image_path=user_image_path, images=images, os=os)




@pages_bp.route('/upload_image', methods=['POST'])
def upload_image():
    try:
        if 'user_id' in session:
            admission_number = session.get('user_id')
            token = session.get('token')

            if not admission_number or not token:
                return jsonify({'error': 'Unauthorized'}), 401

            file = request.files['pics']

            if file:
                # Read the image file data
                image_data = file.read()

                # Create a new image record and associate it with the student
                image = Image(student_admission_number=admission_number, image_data=image_data)
                db.session.add(image)
                db.session.commit()

                # Redirect back to the dashboard
                return redirect(url_for('pages.dashboard'))

            return jsonify({'error': 'No file uploaded'}), 400
    except Exception as e:
        # Log or print the exception for debugging
        print(f"An error occurred: {str(e)}")
        return jsonify({'error': 'File upload failed'}), 500
    
    





@pages_bp.route('/images', methods=['GET'])
def get_image():
    admission_number = request.args.get('admission_number')

    if admission_number:
        # Retrieve the latest image associated with the student
        image = Image.query.filter_by(student_admission_number=admission_number).order_by(Image.created_at.desc()).first()

        if image and image.image_data:
            # Create a Flask response with the image data and set the appropriate content type
            response = make_response(image.image_data)
            response.headers['Content-Type'] = 'image/jpeg'
            return response

    # Handle case where admission_number is not provided or image not found
    return jsonify({'error': 'Image not found'}), 404




@pages_bp.route('/logoutadmin', methods=['GET', 'POST'])
def logoutadmin():
    # Clear the user's session data
    session.clear()

    return redirect(url_for('pages.signinadmin'))





@pages_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    # Clear the user's session data
    session.clear()

    return redirect(url_for('pages.signinstudent'))





def calculate_grade_remark(total_score):
    if total_score >= 70:
        return 'A', 'Excellent'
    elif 65 <= total_score < 70:
        return 'B', 'V. Good'
    elif 60 <= total_score < 65:
        return 'C', 'Good'
    elif 55 <= total_score < 60:
        return 'D', 'Fair'
    elif 50 <= total_score < 55:
        return 'E', 'Pass'
    else:
        return 'F', 'Fail'



@pages_bp.route('/add_scores', methods=['POST'])
def add_scores():
    form = StudentScoreForm()

    if form.validate_on_submit():
        # Retrieve the student and course based on the form data
        student = Student.query.filter_by(admission_number=form.student_id.data).first()
        course = Course.query.filter_by(course_code=form.course_code.data).first()

        if student and course:
            # Calculate total score, grade, and remark
            total_score = form.ca_score.data + form.exam_score.data
            grade, remark = calculate_grade_remark(total_score)

           # Update the existing Course record with the new grades
            course.student_id =  form.student_id.data
            course.course_code = form.course_code.data
            course.ca_score = form.ca_score.data
            course.exam_score = form.exam_score.data
            course.total_score = total_score
            course.grade = grade
            course.remark = remark

            # Commit the changes to the database
            db.session.commit()

            flash('Scores added successfully', 'success')
            return redirect(url_for('pages.admindash'))
        else:
            flash('Invalid student or course ID', 'danger')

    return render_template('pages/admin.html', form=form)







@pages_bp.route('/registerapplicant', methods=['GET','POST'])
def registerapplicant():
    '''
    A function that handles admin registration
    '''
    
    try:
        data = request.form

        existing_email = Applicant.query.filter_by(email=data['email']).first()

        if existing_email:
            return jsonify({'error': 'Email Already Exists!'}), 400
        


        # Create a new user instance
        new_user = Applicant(
            email=data['email'],
            phonenumber=data['phonenumber'],
            password=generate_password_hash(data['password']),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        db.session.add(new_user)
        db.session.commit()

        session['reg_user_id'] = data['email']

        # Return JSON successful message if data's works
        # return redirect('https://paystack.com/pay/vcrh2vy3te')
        return redirect(url_for('pages.form'))     
    
    # Handles database issues (connection or constraint violation)
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    


 

@pages_bp.route('/admissionform', methods=['POST'])
def admission_form():
    '''
    a route that handles the applicant registration form
    '''

    user_email = session.get('reg_user_id')

    if not user_email:
        return redirect(url_for('pages.registerapplicant'))

    if request.method == 'POST':
        applicant_data = request.form.to_dict()
        photograph_file = request.files.get('photograph')

        if photograph_file:
            #save the photograph
            photo_data = photograph_file.read()

            filename = secure_filename(photograph_file.filename)
            photograph_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            applicant_data['photograph'] = photo_data

             # Set the form_number to the user_email
            applicant_data['form_number'] = user_email

         # Check if an admission form already exists for the current user
        existing_form = AdmissionForm.query.filter_by(form_number=user_email).first()

        if existing_form:
            # Update existing form if it already exists
            existing_form.update(**applicant_data)
        else:
            # Create a new form if it doesn't exist
            admission_form = AdmissionForm(**applicant_data)
            db.session.add(admission_form)

        # Commit changes to the database
        db.session.commit()
        return redirect(url_for('pages.success'))
    return render_template('pages/application_form.html')

@pages_bp.route('/success')
def success():
    """
     A Route thats handles the application page
    """
    image4 = os.path.join(current_app.config['UPLOAD_FOLDER'], 'sunnahlogo.jpg')
    
    return render_template('pages/successpage.html', user_image4 = image4)





@pages_bp.route('/applicantboard', methods=['GET'])
@cache.cached(timeout=500)
def applicantboard():
    """
    A Route that handles the admission page
    """
    if 'applicant_user_id' in session:
        email = session.get('applicant_user_id')
        token = session.get('applicant_token')

        if not email or not token:
            return jsonify({'error': 'Unauthorized'}), 401
        
        user = Applicant.query.filter_by(email=email).first()
        
        user_id = user.applicant_number

        if not user:
            return render_template('pages/applicantloginpage.html', message='User not found'), 400

        image4 = os.path.join(current_app.config['UPLOAD_FOLDER'], 'sunnahlogo.jpg')
        # No need to check password here since the user is already authenticated at this point
        return render_template('pages/applicantdashboard.html', user_image=image4, user=user, user_id=user_id)
    # If 'reg_id' is not in the session, it means the user is not logged in
    return redirect(url_for('pages.applicantlogin'))
  


@pages_bp.route('/approve_applicant/<string:email>', methods=['POST'])
def approve_applicant(email):
    # Find the applicant in the database
    applicant = Applicant.query.filter_by(email=email).first()

    if not applicant:
        return jsonify({'error': 'Applicant not found'}), 404

    # Update the admission status to "Approved"
    for form in applicant.applicant_number:
        form.admissionstatus = 'Approved'

    # Commit changes to the database
    db.session.commit()

    # Redirect to dashboard or appropriate page
    return redirect(url_for('pages.specialadmindashboard'))





@pages_bp.route('/reject_applicant/<string:email>', methods=['POST'])
def reject_applicant(email):
    # Find the applicant in the database
    applicant = Applicant.query.filter_by(email=email).first()

    if not applicant:
        return jsonify({'error': 'Applicant not found'}), 404

    # Update the admission status to "Rejected"
    for form in applicant.applicant_number:
        form.admissionstatus = 'Rejected'

    # Commit changes to the database
    db.session.commit()

    # Redirect to dashboard or appropriate page
    return redirect(url_for('pages.specialadmindashboard'))






@pages_bp.route('/delete_applicant/<string:email>', methods=['POST'])
def delete_applicant(email):
    # Find the applicant in the database
    applicant = Applicant.query.filter_by(email=email).first()

    if not applicant:
        return jsonify({'error': 'Applicant not found'}), 404
    
    # Delete the applicant from the database
    db.session.delete(applicant)

    # Commit changes to the database
    db.session.commit()

    # Redirect to dashboard or appropriate page
    return redirect(url_for('pages.specialadmindashboard'))





@pages_bp.route('/view_applicant_info/<email>', methods=['GET'])
def view_applicant_info(email):

    applicant = Applicant.query.filter_by(email=email).first()

    user_id = applicant.applicant_number

    if applicant:
        image1 = os.path.join(current_app.config['UPLOAD_FOLDER'], 'sunnahlogo.jpg')
        return render_template('pages/viewapplicant.html', user_image=image1, applicant=applicant, user_id=user_id)
    else:
        return jsonify({'error': 'Applicant not found'}), 404



@pages_bp.route('/contactmessage', methods=['POST'])
def contactmessage():
    if request.method == 'POST':
        data = request.get_json() 
        name = data.get('name')
        email = data.get('email')
        subject = data.get('subject')
        phone = data.get('phone')
        message = data.get('message')

        # Create a new ContactMessage instance
        new_message = ContactMessage(name=name, email=email, subject=subject, phone=phone, message=message)

        db.session.add(new_message)
        db.session.commit()

        response_message = "Thank you for reaching out to us. Your message has been received, and we assure you that our team will promptly address your inquiry and provide a timely response"
        return jsonify({'message': response_message}), 200



@pages_bp.route('/newsletter', methods=['POST'])
def newsletter():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')

        if not email:
            return jsonify({'error': 'Email address is required'}), 400

        # Create a new Newsletter instance
        subscriber = Newsletter(email=email)

        db.session.add(subscriber)
        db.session.commit()

        response_message = "Thank you for subscribing! We appreciate your support and look forward to providing you with valuable content."
        return jsonify({'message': response_message}), 200


