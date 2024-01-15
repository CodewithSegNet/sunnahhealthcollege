#!/usr/bin/env python3
from flask import current_app, Blueprint, render_template, jsonify, request, url_for, session, redirect, send_file, send_from_directory
from models.student_model import Student
from flask import send_from_directory
from models.image import Image
from app import cache, db
from functools import wraps
import requests
from urllib.parse import quote_plus
import jwt
from io import BytesIO
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import os
import pymysql
from MySQLdb import OperationalError
from dotenv import load_dotenv
import time 


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




# Function to establish a MySQL connection
def connect_to_mysql():
    return pymysql.connect(
        host=os.getenv('DATABASE_HOST'),
        user=os.getenv('DATABASE_USERNAME'),
        passwd=os.getenv('DATABASE_PASSWORD'),
        db=os.getenv('DATABASE')
    )

# Function to reconnect to MySQL if the connection is lost
def mysql_reconnect(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        retry_count = 3  # Number of retry attempts
        while retry_count > 0:
            try:
                db = connect_to_mysql()  # Establish a new connection
                return func(db, *args, **kwargs)
            except OperationalError as e:
                error_code = e.args[0]
                if error_code == 2006:
                    print("MySQL server has gone away. Attempting to reconnect...")
                    time.sleep(1)  # You may adjust the sleep time between retries
                    retry_count -= 1
                else:
                    raise  # Re-raise if it's a different error
        return jsonify({'error': 'Failed to reconnect to the database after multiple attempts.'}), 500
    return wrapper



# Route for handling the student sign-in form submission
@pages_bp.route('/login', methods=['POST'])
@mysql_reconnect
def login(db):
    """
        a route that handles students authentication
    """
    try:
        admission_number = request.form['admission_number']
        password = request.form['password']

        if not admission_number or not password:
            return jsonify({'error': 'Invalid credentials provided.'}), 400


        #Using the provided 'db' connection object to execute the query
        cursor = db.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM students WHERE admission_number = %s LIMIT 1", (admission_number,))
        user = cursor.fetchone()

        if not user:
            return jsonify({'error': 'User not found.'}), 401

        # Check if both admission_number and password are provided
        if not admission_number or not password:
            return jsonify({'error': 'Invalid credentials provided.'}), 400
    
        user = Student.query.filter_by(admission_number=admission_number).first()
        if user and user.check_password(password):
            #Generate JWT token with a configurable expiration time
            expiration_time = datetime.utcnow() + timedelta(hours=2)
            token = jwt.encode({
                'user_id': user.admission_number,
                'exp': expiration_time
            }, current_app.config['SECRET_KEY'], algorithm='HS256')

            # Store token and user ID in the session
            session['token'] = token
            session['user_id'] = user.admission_number

            return redirect(url_for('pages.dashboard'))
        else:
            return jsonify({'error': 'Invalid admission number or password.'}), 401
    except KeyError:
        return jsonify({'error': 'Missing admission number or password in request.'}), 400
    except Exception as e:
        return jsonify({'error': f"An error occurred: {str(e)}"}), 500
    

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
    

    # Retrieve the user's profile image path from the session
    user_image_path = url_for('pages.get_image', admission_number=admission_number)
    
    image1 = os.path.join(current_app.config['UPLOAD_FOLDER'], 'sunnahlogo.jpg')

    return render_template('pages/dashboard.html', student=current_user, departments=departments, semesters=semesters, courses=courses, user_image=image1, user_image_path=user_image_path, os=os)




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



@pages_bp.route('/notfound')
@cache.cached(timeout=500)
def notfound():
    """
     A Route thats handles the 404 page
    """
    image4 = os.path.join(current_app.config['UPLOAD_FOLDER'], 'sunnahlogo.jpg')

    return render_template('pages/404.html', user_image4 = image4)



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



@pages_bp.route('/images')
def get_image():
    admission_number = request.args.get('admission_number')
    
    if admission_number:
        # Encode the admission_number parameter
        encoded_admission_number = quote_plus(admission_number)

        # Retrieve the latest image associated with the student
        image = Image.query.filter_by(student_admission_number=encoded_admission_number).order_by(Image.created_at.desc()).first()

        if image and image.image_data:
            # Send the image data to the client
            return send_file(BytesIO(image.image_data), mimetype='image/jpeg')
    
    # Handle case where admission_number is not provided or image not found
    return jsonify({'error': 'Image not found'}), 404





@pages_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    # Clear the user's session data
    session.clear()

    return redirect(url_for('pages.signinstudent'))
