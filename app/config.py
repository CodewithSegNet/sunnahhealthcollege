#!/usr/bin/env python3

# Imports
import os

# Base class configuration for database
class Config:
    '''
    Base Configuration class
    '''
    SQLALCHRMY_DATABASE_URI = os.environ.get("DATABASE_URL")

    # Disable track modifictions to avoid warning
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    
class DevelopmentConfig(Config):
    '''Development configuration class
    '''
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")

# Mapping config names to their respective classes
config_map = {
        'Development': DevelopmentConfig,
}

# Set the active configuration based on an environment variable
active_env = os.getenv('FLASK_ENV', 'Development')
config = config_map[active_env]