#!/usr/bin/env python3


# Imports
import os
from dotenv import load_dotenv
import pymysql

# Load environment variables from the .env file
load_dotenv()

# Define the absolute path for the upload folder
UPLOAD_FOLDER = 'static/uploads'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# Base class configuration for database
class Config:
    '''
    Base Configuration class
    '''
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{os.getenv('DATABASE_USERNAME')}:{os.getenv('DATABASE_PASSWORD')}@{os.getenv('DATABASE_HOST')}/{os.getenv('DATABASE')}"

    # SQLALCHEMY_DATABASE_URI = f"postgresql://{os.getenv('DATABASE_USERNAME')}:{os.getenv('DATABASE_PASSWORD')}@{os.getenv('DATABASE_HOST')}/{os.getenv('DATABASE')}"


    # Disable track modifictions to avoid warning
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ssl_mode="VERIFY_IDENTITY",
    # ssl={ "ca": "" }


    #Define SSL options in engine options
    SQLALCHEMY_ENGINE_OPTIONS = {
        'connect_args': {
            'ssl': {
                'rejectUnauthorized': True
            }
        }
    }


    # Flask-Caching configuration
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 300
    
class DevelopmentConfig(Config):
    '''Development configuration class
    '''
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")

class TestingConfig(Config):
    '''Testing configuration class
    '''
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") 
    DEBUG = True

class ProductionConfig(Config):
    '''Production configuration class
    '''
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") 
    # SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")

    # Mapping config names to their respective classes
config_map = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}

# Set the active configuration based on an environment variable
active_env = os.getenv('FLASK_ENV', 'testing')
config = config_map[active_env]