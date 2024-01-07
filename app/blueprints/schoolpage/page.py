#!/usr/bin/env python3
from flask import current_app, Blueprint, render_template, jsonify, request, url_for, session, redirect
from app.models.student_model import Student
from flask import send_from_directory
from app.app import cache
from app.config import connect_to_mysql
from functools import wraps
import requests
import jwt
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import os
import MySQLdb
import time 


pages_bp = Blueprint("pages", __name__, template_folder="templates")


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
    # image6 = os.path.join(app.config['UPLOAD_FOLDER'], 'college.jpg')
    # image7 = os.path.join(app.config['UPLOAD_FOLDER'], 'icon-close.svg')
    return render_template('pages/homepage.html', user_image = image1, user_image2 = image2, user_image3 = image3, user_image4 = image4, user_image5 = image5)


# Function to reconnect to MySQL if the connection is lost
def mysql_reconnect(func):
    def wrapper(*args, **kwargs):
        db = connect_to_mysql()  # Create a new connection to MySQL
        while True:
            try:
                return func(db, *args, **kwargs)  # Pass the db connection to the decorated function
            except MySQLdb.OperationalError as e:
                # If MySQL connection is lost, attempt to reconnect
                if e.args[0] in (2006, 2013):  # MySQL server has gone away or Lost connection to MySQL server
                    print("Attempting to reconnect to MySQL...")
                    time.sleep(1)  # Add a delay before reconnection attempt
                    db.close()  # Close the current connection
                    db = connect_to_mysql()  # Reconnect to MySQL
                    print("Reconnected to MySQL")
                else:
                    raise  # Re-raise other OperationalError exceptions
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
        return jsonify({'error': "An error occurred: {}".format(str(e))})
    


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
    user_image2_filename = session.get('user_image2')

    image1 = os.path.join(current_app.config['UPLOAD_FOLDER'], 'sunnahlogo.jpg')

    return render_template('pages/dashboard.html', student=current_user, departments=departments, semesters=semesters, courses=courses, user_image=image1, user_image2=user_image2_filename, os=os)



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
        
            file = request.files['user_image2']

            if file:
                filename = secure_filename(file.filename)
                upload_folder = current_app.config['UPLOAD_FOLDER']
                file.save(os.path.join(upload_folder, filename))
                session['user_image2'] = os.path.join(upload_folder, filename)
                # Update the user's profile image in the database if needed

                # Redirect back to the dashboard or render the dashboard template again
                return redirect(url_for('pages.dashboard'))

            return jsonify({'error': 'No file uploaded'}), 400
    except Exception as e:
        # Log or print the exception for debugging
        print(f"An error occurred: {str(e)}")
        return jsonify({'error': 'File upload failed'}), 500


@pages_bp.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)


@pages_bp.route('/images/<path:filename>')
def get_image(filename):
    return send_from_directory('static/img', filename)




@pages_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    # Clear the user's session data
    session.clear()

    return redirect(url_for('pages.signinstudent'))
