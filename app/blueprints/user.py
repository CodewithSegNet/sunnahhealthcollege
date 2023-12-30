# app/blueprints/user.py

from flask import Blueprint

user_bp = Blueprint('user', __name__)

# Import routes from controllers and define further routes if needed
from app.controllers.models_controller import *
