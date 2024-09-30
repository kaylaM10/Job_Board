from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable = False, unique = True)
    password = db.Column(db.String(120), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def get_json(self):
        return{
            'id': self.id,
            'username': self.username
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

class Job(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(50), nullable = False, unique = True)
    job_description = db.Column(db.String(100), nullable = False,unique = True)
    expected_qualifications = db.Column(db.String(50), nullable = False, unique = True) 

class Applicants(db.Model):
    id =db.Column(db.Integer, primary_key = True)
    job_id = db.Column(db.Integer,db.Foreignkey('job.id'))
    applicant_name = db.Column(db.String(50), nullable = False, unique = True)
    qualifications = db.Column(db.String(50), nullable = False, unique = True) 
