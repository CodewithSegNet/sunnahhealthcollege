#!/usr/bin/env python3
from flask import current_app, Blueprint, render_template, redirect
from run import create_app
import os 


pages_bp = Blueprint("pages", __name__, template_folder="templates")

imageFolder = os.path.join('static', 'img')

app = create_app()

# Access the app's configuration through the 'app' instance
app.config['UPLOAD_FOLDER'] = imageFolder

@pages_bp.route('/home')
def home():
  
    image1 = os.path.join(app.config['UPLOAD_FOLDER'], 'section-img.png')
    image2 = os.path.join(app.config['UPLOAD_FOLDER'], 'slider.jpg')
    image3 = os.path.join(app.config['UPLOAD_FOLDER'], 'student.jpg')
    image4 = os.path.join(app.config['UPLOAD_FOLDER'], 'sunnahlogo.jpg')
    # image5 = os.path.join(app.config['UPLOAD_FOLDER'], 'third.jpg')
    # image6 = os.path.join(app.config['UPLOAD_FOLDER'], 'college.jpg')
    # image7 = os.path.join(app.config['UPLOAD_FOLDER'], 'icon-close.svg')
    return render_template('pages/homepage.html', user_image = image1, user_image2 = image2, user_image3 = image3, user_image4 = image4)
    return render_template('pages/homepage.html')


@pages_bp.route('/signinstudent')
def signinstudent():

    # Access the app's configuration through the 'app' instance
    app.config['UPLOAD_FOLDER'] = imageFolder

    image1 = os.path.join(app.config['UPLOAD_FOLDER'], 'sunnah_college_logo-removebg-preview.png')

    return render_template('pages/signinStudent.html', user_image = image1)



@pages_bp.route('/signinadmin')
def signinadmin():

    # Access the app's configuration through the 'app' instance
    app.config['UPLOAD_FOLDER'] = imageFolder

    image1 = os.path.join(app.config['UPLOAD_FOLDER'], 'sunnah_college_logo-removebg-preview.png')

    return render_template('pages/signinAdmin.html', user_image = image1)
