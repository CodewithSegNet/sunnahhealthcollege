#!/usr/bin/env python3


# Import
from flask import Blueprint, request, session, jsonify
from app.app import create_app, db


# create a blueprint for user related routes
user_bp = Blueprint('user', __name__)


# create a app instance
app = create_app()





