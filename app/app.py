#!/usr/bin/env python3

#imports
from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from app.app.controllers.models_controller import user_bp


# create a sqlalchemy object
db = SQLAlchemy()


def create_app():
    # create an instance of the flask app
    app = Flask(__name__)

    
    # Load configuration from Config class
    app.config.from_object(Config)


    # Initialize the database with the app
    db.init_app(app)


    # Register blueprints
    app.register_blueprint(user_bp, url_prefix='/api')


    # Return the Flask app instance
    return app

if __name__ == '__main__':
    '''
    Create the Flask app by calling the create_app() function
    '''
    app = create_app()

    # Start the Flask app in debug mode
    app.run(debug=True)