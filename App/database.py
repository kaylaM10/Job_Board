from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()


def get_migrate(app):
    return Migrate(app, db)

def create_db(app):
    """Initialize the database with the app and migrate."""
    migrate.init_app(app, db)  
    
    # Create all database tables
    with app.app_context():
        db.create_all()

def init_db(app):
    db.init_app(app)  
    create_db(app)