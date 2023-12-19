#!/usr/bin/env python3
from flask import current_app, Blueprint, render_template, jsonify, request, url_for, session, redirect
from app.models.student_model import Student
from app.app import cache
from functools import wraps
import requests
import jwt
from datetime import datetime, timedelta
import os



pages_bp = Blueprint("pages", __name__, template_folder="templates")


@pages_bp.route('/home')
@cache.cached(timeout=500)
def home():
    """
    A route that handles the app homepage
    """

    image1 = os.path.join(current_app.config['UPLOAD_FOLDER'], 'section-img.png')
    image2 = os.path.join(current_app.config['UPLOAD_FOLDER'], 'slider.jpg')
    image3 = os.path.join(current_app.config['UPLOAD_FOLDER'], 'student.jpg')
    image4 = os.path.join(current_app.config['UPLOAD_FOLDER'], 'sunnahlogo.jpg')
    # image5 = os.path.join(app.config['UPLOAD_FOLDER'], 'third.jpg')
    # image6 = os.path.join(app.config['UPLOAD_FOLDER'], 'college.jpg')
    # image7 = os.path.join(app.config['UPLOAD_FOLDER'], 'icon-close.svg')
    return render_template('pages/homepage.html', user_image = image1, user_image2 = image2, user_image3 = image3, user_image4 = image4)



# Route for handling the student sign-in form submission
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
            return jsonify({'error': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'error': "An error occured: {}".format(str(e))})
    


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
    user_id = session.get('user_id')
    token = session.get('token')

    if not user_id or not token:
        return jsonify({'error': 'Unauthorized'}), 401
    
    current_user = Student.query.get(user_id)
    

    image1 = os.path.join(current_app.config['UPLOAD_FOLDER'], 'sunnahlogo.jpg')
    image2 = os.path.join(current_app.config['UPLOAD_FOLDER'], 'student.jpg')


    return render_template('pages/dashboard.html', student=current_user, user_image=image1, user_image2=image2)



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



