#!/usr/bin/env python3
from flask import current_app, render_template, redirect, url_for, session
import os
from app import cache, db
from controllers.pageroute import pages_bp, payment_required




@pages_bp.route('/sign_in_student')
def signinstudent():
    """
     A Route thats handles the StudentSignIn
    """

    image1 = os.path.join(current_app.config['UPLOAD_FOLDER'], 'sunnah_college_logo-removebg-preview.png')

    return render_template('signin_student.html', user_image = image1)



@pages_bp.route('/sign_in_admin')
def signinadmin():

    image1 = os.path.join(current_app.config['UPLOAD_FOLDER'], 'sunnah_college_logo-removebg-preview.png')

    return render_template('signin_admin.html', user_image = image1)





@pages_bp.route('/contact')
@cache.cached(timeout=500)
def contact():
    """
     A Route thats handles the StudentSignIn
    """

    image1 = os.path.join(current_app.config['UPLOAD_FOLDER'], 'section-img.png')
    image4 = os.path.join(current_app.config['UPLOAD_FOLDER'], 'sunnah_college_logo-removebg-preview.png')

    return render_template('contact.html',  user_image = image1, user_image4 = image4)


@pages_bp.route('/admission')
@cache.cached(timeout=500)
def admission():
    """
     A Route thats handles the admission page
    """

    image4 = os.path.join(current_app.config['UPLOAD_FOLDER'], 'sunnah_college_logo-removebg-preview.png')

    return render_template('admission.html', user_image4 = image4)






@pages_bp.route('/history')
@cache.cached(timeout=500)
def history():
    """
     A Route thats handles the history page
    """

    image4 = os.path.join(current_app.config['UPLOAD_FOLDER'], 'sunnah_college_logo-removebg-preview.png')
    
    return render_template('history.html', user_image4 = image4)




@pages_bp.route('/vision')
@cache.cached(timeout=500)
def vision():
    """
     A Route thats handles the vision page
    """

    image4 = os.path.join(current_app.config['UPLOAD_FOLDER'], 'sunnah_college_logo-removebg-preview.png')

    return render_template('vision.html', user_image4 = image4)



@pages_bp.route('/programmes')
@cache.cached(timeout=500)
def programmes():
    """
     A Route thats handles the programmes page
    """

    image4 = os.path.join(current_app.config['UPLOAD_FOLDER'], 'sunnah_college_logo-removebg-preview.png')
    
    return render_template('programmes.html', user_image4 = image4)



@pages_bp.route('/application')
@cache.cached(timeout=500)
def application():
    """
     A Route thats handles the application page
    """
    image4 = os.path.join(current_app.config['UPLOAD_FOLDER'], 'sunnah_college_logo-removebg-preview.png')
    
    return render_template('application.html', user_image4 = image4)




@pages_bp.route('/form')
@cache.cached(timeout=500)
def form():
    """
     A Route thats handles the application page
    """
    image4 = os.path.join(current_app.config['UPLOAD_FOLDER'], 'sunnah_college_logo-removebg-preview.png')
    
    return render_template('application_form.html', user_image = image4)



@pages_bp.route('/not_found')
@cache.cached(timeout=500)
def notfound():
    """
     A Route thats handles the 404 page
    """
    image4 = os.path.join(current_app.config['UPLOAD_FOLDER'], 'sunnah_college_logo-removebg-preview.png')

    return render_template('404.html', user_image4 = image4)



@pages_bp.route('/applicant')
@payment_required
def applicant():
    """
     A Route thats handles the application page
    """
    image4 = os.path.join(current_app.config['UPLOAD_FOLDER'], 'sunnah_college_logo-removebg-preview.png')
    
    return render_template('applicant.html', user_image4 = image4)




@pages_bp.route('/applicant_login')
def applicantlogin():
    """
     A Route thats handles the application page
    """
    image4 = os.path.join(current_app.config['UPLOAD_FOLDER'], 'sunnah_college_logo-removebg-preview.png')
    
    return render_template('applicant_login_page.html', user_image4 = image4)





@pages_bp.route('/special_login')
def speciallog():
    """
     A Route thats handles the application page
    """
    image4 = os.path.join(current_app.config['UPLOAD_FOLDER'], 'sunnah_college_logo-removebg-preview.png')
    
    return render_template('special.html', user_image4 = image4)



@pages_bp.route('/logout_admin', methods=['GET', 'POST'])
def logoutadmin():
    # Clear the user's session data
    session.clear()

    return redirect(url_for('pages.signinadmin'))





@pages_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    # Clear the user's session data
    session.clear()

    return redirect(url_for('pages.signinstudent'))





@pages_bp.route('/success')
def success():
    """
     A Route thats handles the application page
    """
    image4 = os.path.join(current_app.config['UPLOAD_FOLDER'], 'sunnah_college_logo-removebg-preview.png')
    
    return render_template('successful_page.html', user_image4 = image4)





# /****************************************** ROUTES ************************************************/



