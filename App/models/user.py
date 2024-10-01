from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from App.database import db

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String(20), nullable=False, unique=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable = False, unique = True)
    password = db.Column(db.String(120), nullable=False)

    def __init__(self, username, password, first_name, last_name):
        self.username = username
        self.set_password(password)
        self.first_name = first_name
        self.last_name = last_name

    def get_json(self):
        return{
            'id': self.id,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

class Job(db.Model):
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(100), nullable = False, unique = True)
    description = db.Column(db.String(1000), nullable = False,unique = True)
    expected_qualifications = db.Column(db.String(50), nullable = False, unique = True) 

def __init__(self, user_id, title,description, expected_qualifications):
    self.user_id = user_id
    self.title = title
    self.description = description
    self.expected_qualifications = expected_qualifications

def get_json(self):
    return{
        'id': self.id,
        'user_id': self.user_id,
        'title': self.title,
        'description':self.description,
        'expected_qualifications': self.expected_qualifications
    }

class Applicant(db.Model):
    __tablename__ = 'applicants'
    id =db.Column(db.Integer, primary_key = True)
    job_id = db.Column(db.Integer,db.Foreignkey('job.id'))
    user_id = db.Column(db.Integer,db.Foreignkey('user.id'))
    applicant_name = db.Column(db.String(50), nullable = False, unique = True)
    qualifications = db.Column(db.String(50), nullable = False, unique = True)
    status = db.Column(db.String(50), default='applied')  
    cover_letter = db.Column(db.Text, nullable=True)   

def __init__(self, user_id, job_id, qualifications,status,cover_letter):
    self.user_id = user_id
    self.job_id = job_id
    self.qualifications = qualifications
    self.status = status
    self.cover_letter = cover_letter


def get_json(self):
    return{
        'id': self.id,
        'user_id': self.user_id,
        'job_id': self.job_id,
        'qualifications': self.qualifications,
        'status': self.status,
        'cover_letter':self.cover_letter
    }