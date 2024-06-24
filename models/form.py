#!/usr/bin/env python3

# Import
from app import db
import models.applicant
from models.form_image import FormImage
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class AdmissionForm(db.Model):

    __tablename__ = 'admissionforms'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=True)
    form_number = db.Column(db.String(255), db.ForeignKey('applicants.email'))
    fullnames = db.Column(db.String(100), nullable=True)
    contactaddress = db.Column(db.String(200), nullable=True)
    maritalstatus = db.Column(db.String(50), nullable=True)
    stateoforigin = db.Column(db.String(50), nullable=True)
    emailaddress = db.Column(db.String(100), nullable=True)
    dateofbirth = db.Column(db.Date, nullable=True)
    lastschoolattended = db.Column(db.String(100), nullable=True)
    phonenumber = db.Column(db.String(20), nullable=True)
    admissionstatus = db.Column(db.String(20), default='In Progress', nullable=True)
    
    # Course applying
    courses = db.Column(db.String(255), nullable=True)

    # Next of Kin
    nextofkinname = db.Column(db.String(100), nullable=True)
    nextofkinaddress = db.Column(db.String(200), nullable=True)
    kinstateoforigin = db.Column(db.String(50), nullable=True)
    nextofkinphonenumber = db.Column(db.String(20), nullable=True)

    # Name of Parent/Guardian
    parentguardianname = db.Column(db.String(100), nullable=True)
    parentguardianaddress = db.Column(db.String(200), nullable=True)
    placeofbirthparent = db.Column(db.String(50), nullable=True)
    parentstateoforigin = db.Column(db.String(20), nullable=True)
    parentguardianphonenumber = db.Column(db.String(20), nullable=True)


    # Schools attended
    school1 = db.Column(db.String(100), nullable=True)
    from1 = db.Column(db.Date, nullable=True)
    to1 = db.Column(db.Date, nullable=True)
    certificate1 = db.Column(db.String(50), nullable=True)

    school2 = db.Column(db.String(100), nullable=True)
    from2 = db.Column(db.Date, nullable=True)
    to2 = db.Column(db.Date, nullable=True)
    certificate2 = db.Column(db.String(50), nullable=True)

    school3 = db.Column(db.String(100), nullable=True)
    from3 = db.Column(db.Date, nullable=True)
    to3 = db.Column(db.Date, nullable=True)
    certificate3 = db.Column(db.String(50), nullable=True)


    # Detailed Results
    examination = db.Column(db.String(10), nullable=True)




    subject1 = db.Column(db.String(100), nullable=True)
    sgrade1 = db.Column(db.String(10), nullable=True)
    subject2 = db.Column(db.String(100), nullable=True)
    sgrade2 = db.Column(db.String(10), nullable=True)
    subject3 = db.Column(db.String(100), nullable=True)
    sgrade3 = db.Column(db.String(10), nullable=True)
    subject4 = db.Column(db.String(100), nullable=True)
    sgrade4 = db.Column(db.String(10), nullable=True)
    subject5 = db.Column(db.String(100), nullable=True)
    sgrade5 = db.Column(db.String(10), nullable=True)
    subject6 = db.Column(db.String(100), nullable=True)
    sgrade6 = db.Column(db.String(10), nullable=True)
    subject7 = db.Column(db.String(100), nullable=True)
    sgrade7 = db.Column(db.String(10), nullable=True)
   






    # National Diploma Detailed Result
    national_diploma_subject_1 = db.Column(db.String(100), nullable=True)
    grade1 = db.Column(db.String(10), nullable=True)
    national_diploma_subject_2 = db.Column(db.String(100), nullable=True)
    grade2 = db.Column(db.String(10), nullable=True)
    national_diploma_subject_3 = db.Column(db.String(100), nullable=True)
    grade3 = db.Column(db.String(10), nullable=True)
    national_diploma_subject_4 = db.Column(db.String(100), nullable=True)
    grade4 = db.Column(db.String(10), nullable=True)
    national_diploma_subject_5 = db.Column(db.String(100), nullable=True)
    grade5 = db.Column(db.String(10), nullable=True)
    national_diploma_subject_6 = db.Column(db.String(100), nullable=True)
    grade6 = db.Column(db.String(10), nullable=True)

    # Record of Employment
    employmentSector1 = db.Column(db.String(100), nullable=True)
    postHeld1 = db.Column(db.String(100), nullable=True)
    employmentDate1 = db.Column(db.String(20), nullable=True)

    employmentSector2 = db.Column(db.String(100), nullable=True)
    postHeld2 = db.Column(db.String(100), nullable=True)
    employmentDate2 = db.Column(db.String(20), nullable=True)

    employmentSector3 = db.Column(db.String(100), nullable=True)
    postHeld3 = db.Column(db.String(100), nullable=True)
    employmentDate3 = db.Column(db.String(20), nullable=True)

    # List of Credentials
    credential1 = db.Column(db.String(100), nullable=True)
    credential2 = db.Column(db.String(100), nullable=True)
    credential3 = db.Column(db.String(100), nullable=True)
    credential4 = db.Column(db.String(100), nullable=True)
    credential5 = db.Column(db.String(100), nullable=True)

    # Sponsorship
    sponsorship = db.Column(db.String(20), nullable=True)
    sponsorname = db.Column(db.String(100), nullable=True)
    sponsoraddress = db.Column(db.String(200), nullable=True)

    responsibleparty = db.Column(db.String (255), nullable=True)
    convicted = db.Column(db.String(255), nullable=True)
    declarationparta = db.Column(db.String(255), nullable=True)
    declarationpartb = db.Column(db.String(255), nullable=True)
    declarationpartc = db.Column(db.String(255), nullable=True)


    
    # Relationship with images
    photograph = db.relationship('FormImage', backref='applicant_number', lazy=True)

    # Define the relationship with Applicant
    applicant = db.relationship('Applicant', back_populates='applicant_number', overlaps="admission_forms, applicant")


    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        