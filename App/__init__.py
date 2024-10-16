from flask import Flask
from App.database import db

# Importing necessary components
from .models import *  
from .views import *   
from .controllers import *  
from .main import *     

def create_app(overrides={}):
    app = Flask(__name__, static_url_path='/static')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'your_database_uri_here'  # Use your main database URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)  # Initialize the db with your app
    return app