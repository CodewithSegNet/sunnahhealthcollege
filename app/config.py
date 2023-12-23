#!/usr/bin/env python3


# Imports
import os


# Define the absolute path for the upload folder
UPLOAD_FOLDER = 'static/img'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# Base class configuration for database
class Config:
    '''
    Base Configuration class
    '''
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")

    # Disable track modifictions to avoid warning
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    

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

    # Mapping config names to their respective classes
config_map = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}

# Set the active configuration based on an environment variable
active_env = os.getenv('FLASK_ENV', 'testing')
config = config_map[active_env]