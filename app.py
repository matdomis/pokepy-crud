from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager    #type: ignore
from flask_bcrypt import Bcrypt         #type: ignore

import os

db = SQLAlchemy()

DATABASE_URL = os.getenv('DATABASE_URL')
FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY')

def create_app():
    """
        Create and configure the Flask application instance. 

        The application is using the 'App Factory' pattern.

        This function initializes the Flask app with the following configurations:
            - Database: Configures SQLAlchemy to connect to a PostgreSQL database using the provided `DB_PASSWORD`.
            - Secret Key: Sets the Flask app's secret key for session management.
            - Database Initialization: Initializes the database connection with SQLAlchemy.
            - Login Manager: Configures Flask-Login to manage user authentication and session handling.
            - User Loader: Loads the user object from the database based on the user ID.
            - Unauthorized Handler: Redirects unauthorized users to the login page.
            - Views: Imports and sets up the routes and views for the application.
            - Password Hashing: Configures Bcrypt for password hashing.
            - Database Migration: Sets up Flask-Migrate for handling database migrations.

    """

    app = Flask(__name__, template_folder='templates', static_folder='static')

    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = FLASK_SECRET_KEY

    db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    
    from models import User

    @login_manager.user_loader
    def load_user(uid):
        return User.query.get(uid)

    @login_manager.unauthorized_handler
    def unauthorized_callback():
        return redirect(url_for('login'))

    bcrypt = Bcrypt(app)

    from views import generate_views

    generate_views(app, db, bcrypt)

    migrate = Migrate(app, db)

    return app