import os
import logging
from flask import Flask, render_template
from flask_uploads import DOCUMENTS, IMAGES, TEXT, UploadSet, configure_uploads
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage

from App.database import init_db
from App.config import load_config
from App.controllers import setup_jwt, add_auth_context
from App.views import views, setup_admin

def add_views(app):
    for view in views:
        app.register_blueprint(view)

def create_app(overrides={}):
    app = Flask(__name__, static_url_path='/static')
    
    load_config(app, overrides)
    
    CORS(app)
    
    # Set up logging
    logging.basicConfig(level=logging.INFO)  # Set the logging level to INFO
    logger = logging.getLogger(__name__)  # Create a logger for this module
    logger.info("Creating Flask application.")

    # Set up JWT for authentication
    add_auth_context(app)

    app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(app.instance_path, 'uploads/photos')
    app.config['UPLOADED_DOCUMENTS_DEST'] = os.path.join(app.instance_path, 'uploads/documents')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Optional, but recommended

    # Set up file uploads
    photos = UploadSet('photos', TEXT + DOCUMENTS + IMAGES)
    configure_uploads(app, photos)

    # Create instance path if it does not exist
    if not os.path.exists(app.instance_path):
        os.makedirs(app.instance_path)
        logger.info("Created instance path at: %s", app.instance_path)  # Log instance path creation

    # Add views (Blueprints)
    add_views(app)

    # Initialize the database
    init_db(app)
    logger.info("Database initialized.")  # Log database initialization

    # Set up JWT
    jwt = setup_jwt(app)
    setup_admin(app)

    @jwt.invalid_token_loader
    @jwt.unauthorized_loader
    def custom_unauthorized_response(error):
        return render_template('401.html', error=error), 401

    app.app_context().push()
    return app