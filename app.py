#!/usr/bin/env python3

# imports
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from decouple import config
from flask_cors import CORS
import os


# create a sqlalchemy object
db = SQLAlchemy()

# create a cache object
cache = Cache()


def create_app():
    # create an instance of the flask app
    app = Flask(__name__)

    # Load configuration from Config class
    app.config.from_object(Config)

    # Initialize Flask-caching
    cache.init_app(app)

    # Initialize the database with the app
    db.init_app(app)

    # secret key from the .env file using python-decouple
    secret_key = config("SECRET_KEY")
    PAYSTACK_SECRET_KEY = os.getenv("PAYSTACK_SECRET_KEY")

    # set key for app
    app.secret_key = secret_key

    # Access the app's configuration through the 'app' instance
    app.config["UPLOAD_FOLDER"] = os.path.join("static", "img")

    from controllers import register_blueprints

    register_blueprints(app)

    # create the datebase tables
    with app.app_context():
        db.create_all()

    # Configure CORS to allow requests from any origin
    CORS(app, supports_credentials=True)

    # Return the Flask app instance
    return app


if __name__ == "__main__":
    """
    Create the Flask app by calling the create_app() function
    """
    app = create_app()

    # Start the Flask app in debug mode
    app.run(debug=True)
