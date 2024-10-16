from flask import Flask
from App.database import db, create_db

def create_app():
    app = Flask(__name__)

    # Load configuration from a config file or directly here
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///temp-database.db'  
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  
    app.config['SECRET_KEY'] = 'secret key'  

    # Initialize the database with the app
    create_db(app)

    return app