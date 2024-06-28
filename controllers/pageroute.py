
#!/usr/bin/env python3
from flask import current_app, Blueprint, render_template, jsonify, request, url_for, session, redirect, send_file, send_from_directory, make_response, flash
from functools import wraps
from config import UPLOAD_FOLDER, allowed_file
import json
import traceback
import base64
import requests
from urllib.parse import quote, unquote
import jwt
import logging
from io import BytesIO
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import SQLAlchemyError
import os
import pymysql
from MySQLdb import OperationalError
from dotenv import load_dotenv
import time 
import traceback
from models import Student, Department, Semester, ContactMessage, Admin, AdmissionForm, FormImage, Newsletter, Specialadmin, Applicant, Image, Course, PaymentStatus
from controllers import StudentScoreForm
from app import cache, db
from views import *





# Set up logging
logging.basicConfig(level=logging.DEBUG)


# /****************************************** GLOBAL ROUTES ************************************************/


pages_bp = Blueprint("pages", __name__, template_folder="templates")




# Load environment variables from the .env file
load_dotenv()


# Print loaded environment variables
print(os.getenv('PAYSTACK_SECRET_KEY'))



@pages_bp.route('/')
@cache.cached(timeout=500)
def home():
    """
    A route that handles the app homepage
    """

    image1 = os.path.join(current_app.config['UPLOAD_FOLDER'], 'section-img.png')
    image2 = os.path.join(current_app.config['UPLOAD_FOLDER'], 'slider.jpg')
    image3 = os.path.join(current_app.config['UPLOAD_FOLDER'], 'student.webp')
    image4 = os.path.join(current_app.config['UPLOAD_FOLDER'], 'sunnahlogo.avif')
    image5 = os.path.join(current_app.config['UPLOAD_FOLDER'], 'sunPics1.webp')
    image6 = os.path.join(current_app.config['UPLOAD_FOLDER'], 'sunPics2.webp')
    # image7 = os.path.join(app.config['UPLOAD_FOLDER'], 'icon-close.svg')
    return render_template('homepage.html', user_image = image1, user_image2 = image2, user_image3 = image3, user_image4 = image4, user_image5 = image5, user_image6 = image6)



# /****************************************** VIEWS ROUTES ************************************************/





# /****************************************** STUDENT LOGIN & LOGIC ROUTES ************************************************/



@pages_bp.route('/payment_callback', methods=['GET'])
def paymentCallback():
    reference = request.args.get('reference')
    logging.debug("Reference: %s", reference)

    if not reference:
        logging.error("No reference provided")
        return "No reference provided", 400

    # Verify User payment
    try:
        response = requests.get(f'https://api.paystack.co/transaction/verify/{reference}', 
                                headers={'Authorization': f"Bearer {os.getenv('PAYSTACK_SECRET_KEY')}"})
        logging.debug("Paystack Response: %s", response.text)
    except requests.RequestException as e:
        logging.error("RequestException during Paystack verification: %s", e)
        return "Failed to verify payment with Paystack", 500

    if response.status_code == 200:
        data = response.json().get('data', {})
        status = data.get('status')
        if status == 'success':
            customer = data.get('customer', {})
            email = customer.get('email')
            if email:
                logging.debug("Email: %s", email)

                # Store user payment credentials in session
                session['email'] = email
                session['is_paid'] = True

                # Check if the user already exists in the database
                user = PaymentStatus.query.filter_by(email=email).first()
                if user:
                    user.is_paid = True
                    db.session.commit()
                else:
                    # Create a new Paymentstatus if it doesn't exist
                    new_user = PaymentStatus(email=email, is_paid=True)
                    db.session.add(new_user)
                    db.session.commit()
                    logging.info("New PaymentStatus entry created for email: %s", email)

                return redirect(url_for('pages.applicant'))
            else:
                logging.error("Email not found in Paystack response")
                return "Email not found in Paystack response", 400
        else:
            logging.error("Payment verification failed: %s", status)
            return f"Payment verification failed: {status}", 400
    else:
        logging.error("Failed to verify payment with Paystack, status code: %d", response.status_code)
        return "Failed to verify payment with Paystack", 400


def payment_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        email = session.get('email')
        is_paid = session.get('is_paid')
        current_app.logger.debug(f"email in session: {email}, is_paid: {is_paid}")

        if not email or not is_paid:
            return redirect(url_for('pages.admission'))

        user = PaymentStatus.query.filter_by(email=email).first()

        if not user or not user.is_paid:
            current_app.logger.debug("User not found or not paid in database")
            return redirect(url_for('pages.payment_callback'))

        return f(*args, **kwargs)
    return decorated_function







@pages_bp.route('/store_payment_status', methods=['POST'])
def store_payment_status():
    data = request.json
    if 'email' not in data or 'is_paid' not in data:
        return jsonify({'error': 'Email and is_paid fields are required'}), 400

    email = data['email']
    is_paid = data['is_paid']

    try:
        user = PaymentStatus.query.filter_by(email=email).first()
        if user:
            # Update the payment status if the user already exists
            user.is_paid = is_paid
        else:
            # Create a new user entry if the user doesn't exist
            user = PaymentStatus(email=email, is_paid=is_paid)
            db.session.add(user)

        db.session.commit()
        return jsonify({'message': 'Payment status stored successfully'}), 200

    except Exception as e:
        db.session.rollback()
        logging.error("Error storing payment status: %s", e)
        return jsonify({'error': 'Failed to store payment status'}), 500






    
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
            flash('Incorrect admission number or password. Please try agin.', 'danger')
            return redirect(url_for('pages.signinstudent'))    
    except Exception as e:
        flash("An error occured: {}".format(str(e)), 'danger'), 500
        return redirect(url_for('pages.signinstudent'))    

    






# /****************************************** END OF HOMEPAGE & LOGIC ROUTES ************************************************/





# /****************************************** ADMIN ROUTES ************************************************/



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
            flash('Incorrect email or password. Please try agin.', 'danger')
            return redirect(url_for('pages.signinadmin'))
    except Exception as e:
        traceback.print_exc()
        flash(f'An error occurred: {str(e)}', 'danger'), 500
        return redirect(url_for('pages.signinadmin'))





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


# /****************************************** END OF  ADMIN ROUTES ************************************************/





# /****************************************** APPLICANT & APPLICANT ADMIN ROUTES ************************************************/

@pages_bp.route('/applicant_page', methods=['POST', 'GET'])
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
            flash('Incorrect email or password. Please try agin.', 'danger')
            return redirect(url_for('pages.applicantlogin'))
    except Exception as e:
        traceback.print_exc()
        flash(f'An error occurred: {str(e)}', 'danger'), 500
        return redirect(url_for('pages.applicantlogin'))

# /****************************************** ENO APPLICANT & APPLICANT ADMIN ROUTES ************************************************/





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






@pages_bp.route('/admin_dashboard', methods=['GET'])
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

        image1 = os.path.join(current_app.config['UPLOAD_FOLDER'], 'sunnahlogo.avif')

        form = StudentScoreForm()

        return render_template('admin.html', user=user, user_image=image1, os=os, student_info=student_info, image_info=image_info, form=form)
    else:
        return jsonify({'error': 'Unauthorized'}), 401






@pages_bp.route('/special_admin', methods=['POST', 'GET'])
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
            flash('Incorrect email or password. Please try agin.', 'danger')
            return redirect(url_for('pages.speciallog'))
    except Exception as e:
        traceback.print_exc()
        flash(f'An error occurred: {str(e)}', 'danger'), 500
        return redirect(url_for('pages.speciallog'))




def get_latest_image_info(email):
    if email:
        # Retrieve the latest image associated with the applicant
        form = AdmissionForm.query.filter_by(form_number=email).order_by(AdmissionForm.id.desc()).first()

        if form:
            image = FormImage.query.filter_by(form_id=form.id).order_by(FormImage.created_at.desc()).first()

            if image and image.image_data:
                return {
                    'image_data': image.image_data,
                    'mimetype': 'image/jpeg',
                }

    return None




@pages_bp.route('/special_admin_dashboard', methods=['GET'])
def specialadmindashboard():
    if 'special_user_id' in session:
        email = session.get('special_user_id')
        token = session.get('special_token')

        if not email or not token:
            return jsonify({'error': 'Unauthorized'}), 401

        user = Specialadmin.query.filter_by(email=email).first()

        # Fetch applicants
        applicants = Applicant.query.options(db.joinedload(Applicant.applicant_number)).all()

        # Fetch images for each applicant
        applicants_with_images = []
        for applicant in applicants:
            form_number = applicant.email
            image_info = get_latest_image_info(form_number)
            if image_info:
                image_path = image_info['image_data'].decode('utf-8') if isinstance(image_info['image_data'], bytes) else image_info['image_data']
                # Ensure the path does not include "static/" prefix twice
                if image_path.startswith("static/"):
                    image_path = image_path[7:]
                applicant_image = image_path
            else:
                applicant_image = None

            applicants_with_images.append({
                'applicant': applicant,
                'image': applicant_image,
                'forms': applicant.applicant_number
            })

        image1 = os.path.join(current_app.config['UPLOAD_FOLDER'], 'sunnah_college_logo-removebg-preview.png')

        return render_template('special_dashboard.html', user=user, user_image=image1, applicants=applicants_with_images)
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

    
    print("Image file exists:", os.path.exists(user_image_path))
    print("User Image Path:", user_image_path)

      
    
    image1 = os.path.join(current_app.config['UPLOAD_FOLDER'], 'sunnahlogo.avif')

    return render_template('dashboard.html', student=current_user, departments=departments, semesters=semesters, courses=courses, user_image=image1, user_image_path=user_image_path, images=images, os=os)




@pages_bp.route('/upload_image', methods=['POST'])
def upload_image():
    try:
        if 'user_id' in session:
            admission_number = session.get('user_id')
            token = session.get('token')

            if not admission_number or not token:
                return jsonify({'error': 'Unauthorized'}), 401

            file = request.files['pics']

            if file and allowed_file(file.filename):
                filename = file.filename
                image_data = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                file.save(image_data)

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

            # Open the image file and read its content
            with open(image.image_data, 'rb') as f:
                image_data = f.read()

            # Create a Flask response with the image data and set the appropriate content type
            response = make_response(image_data)
            response.headers['Content-Type'] = 'image/jpeg'
            
            print("Response:", response)
            print("Headers:", response.headers)

            return response

    # Handle case where admission_number is not provided or image not found
    return jsonify({'error': 'Image not found'}), 404










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




















@pages_bp.route('/register_applicant', methods=['GET', 'POST'])
def registerapplicant():
    '''
    A function that handles admin registration
    '''
    
    if request.method == 'POST':
        try:
            if not session.get('is_paid'):
                return jsonify({'error': 'Payment not verified'}), 400
            
            
            data = request.form
            email = session.get('email')
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
                is_paid = True
            )

            db.session.add(new_user)
            db.session.commit()


            #clear email and payment status from session
            session.pop('email', None)
            session.pop('is_paid', None)

            session['reg_user_id'] = data['email']

            # Return JSON successful message if data's works
            return redirect(url_for('pages.form'))     
        
        # Handles database issues (connection or constraint violation)
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
        















@pages_bp.route('/admission_form', methods=['POST'])
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

        if photograph_file and allowed_file(photograph_file.filename):
            # save the photograph
            filename = secure_filename(photograph_file.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            photograph_file.save(filepath)            
            # Ensure user_email is not None before setting form_number
            if user_email:
                # Set the form_number to the user_email
                applicant_data['form_number'] = user_email

            # Check if an admission form already exists for the current user
            existing_form = AdmissionForm.query.filter_by(form_number=user_email).first()

            if existing_form:
                form_id = existing_form.id
            else:
                # Create a new form if it doesn't exist
                admission_form = AdmissionForm(**applicant_data)
                db.session.add(admission_form)
                db.session.commit()  # Commit the AdmissionForm
                form_id = admission_form.id  # Get the form_id

            # Create a new FormImage instance with the form_id
            form_image = FormImage(form_id=form_id, image_data=filepath)
            db.session.add(form_image)
        
        # Commit changes to the database
        db.session.commit()
        
        return redirect(url_for('pages.success'))
    
    return render_template('application_form.html')












@pages_bp.route('/applicant_board', methods=['GET'])
@cache.cached(timeout=500)  # Assuming you're using caching
def applicantboard():
    """
    Route that handles the applicant dashboard page.
    """
    if 'applicant_user_id' in session:
        email = session.get('applicant_user_id')
        token = session.get('applicant_token')

        if not email or not token:
            return jsonify({'error': 'Unauthorized'}), 401
        
        # Retrieve applicant details from database
        user = Applicant.query.filter_by(email=email).first()

        if not user:
            return render_template('applicant_login_page.html', message='User not found'), 400
        
        # Fetch applicant number or other necessary details
        user_id = user.applicant_number 
        
        # Assuming you have a function like get_latest_image_info
        image_info = get_latest_image_info(user.email)  
        
        if image_info:
            image_path = image_info['image_data'].decode('utf-8') if isinstance(image_info['image_data'], bytes) else image_info['image_data']
            if image_path.startswith("static/"):
                image_path = image_path[7:]
            applicant_image = image_path
        else:
            applicant_image = 'sunnah_college_logo-removebg-preview.png'
        
        # Example default image if applicant_image is None
        user_image = os.path.join(current_app.config['UPLOAD_FOLDER'], 'sunnahlogo.avif')

        # Render the template with the necessary data
        return render_template('applicant_dashboard.html', user=user, user_id=user_id, applicant_image=applicant_image, user_image=user_image)
    
    # If 'applicant_user_id' is not in the session, redirect to login
    return redirect(url_for('pages.applicant_login'))
  





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
    
    if applicant:
        form_number = applicant.email
        image_info = get_latest_image_info(form_number)
        if image_info:
            image_path = image_info['image_data'].decode('utf-8') if isinstance(image_info['image_data'], bytes) else image_info['image_data']
            if image_path.startswith("static/"):
                image_path = image_path[7:]
            applicant_image = image_path
        else:
            applicant_image = 'sunnah_college_logo-removebg-preview.png'
        
        user_id = applicant.applicant_number
        
        return render_template('view_applicant.html', user_image=applicant_image, applicant=applicant, user_id=user_id)
    else:
        return jsonify({'error': 'Applicant not found'}), 404



@pages_bp.route('/view_image/<image_id>', methods=['GET'])
def view_image(image_id):
    form_image = FormImage.query.get(image_id)
    if form_image:
        response = make_response(form_image.image_data)
        response.headers['Content-Type'] = 'image/jpeg'

    else:
        return 'Image not found', 404




@pages_bp.route('/contact_message', methods=['POST'])
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





