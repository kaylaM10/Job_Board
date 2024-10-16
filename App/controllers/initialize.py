from App.database import db
from App.models import User, Job  # Make sure to import your models
from .user import create_user  # Import your user creation function
import logging

LOGGER = logging.getLogger(__name__)

def initialize():
    try:
        db.drop_all()  # Drop all existing tables
        db.create_all()  # Create all tables
        LOGGER.info("Database tables dropped and recreated.")
        
        # Create initial users 
        create_user('bob', 'bobpass', 'Bob', 'Builder', 'bob@example.com')  
        create_user('alice', 'alicepass', 'Alice', 'Smith', 'alice@example.com')  

        LOGGER.info("Initial users created.")

        LOGGER.info("Initialization complete.")
    except Exception as e:
        LOGGER.error(f"Error during initialization: {e}")