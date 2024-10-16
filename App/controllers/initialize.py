from App.database import db
from App.models import User, Job  # Make sure to import your models
from .user import create_user  # Import your user creation function
import logging

LOGGER = logging.getLogger(__name__)

def initialize():
    # Set up the database
    try:
        db.drop_all()  # Drop all existing tables
        db.create_all()  # Create all tables defined in your models
        LOGGER.info("Database tables dropped and recreated.")
        
        # Create initial users if needed
        create_user('bob', 'bobpass', 'Bob', 'Builder')  # Include first_name and last_name if necessary
        create_user('alice', 'alicepass', 'Alice', 'Smith')  # Another example user

        LOGGER.info("Initial users created.")
        
        # If you need to create jobs or other entities, do that here as well
        # Example:
        # job = Job(title="Software Engineer", description="Develop applications", user_id=1)
        # db.session.add(job)
        # db.session.commit()

        LOGGER.info("Initialization complete.")
    except Exception as e:
        LOGGER.error(f"Error during initialization: {e}")