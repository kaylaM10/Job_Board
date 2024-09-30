from App.models import User,Job,Applicant
from App.database import db
from flask_jwt_extended import create_access_token

def create_user(username, password):
    newuser = User(username=username, password=password)
    newuser.set_password(password)
    db.session.add(newuser)
    db.session.commit()
    return newuser

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def get_user(id):
    return User.query.get(id)

def get_all_users():
    return User.query.all()

def get_all_users_json():
    users = User.query.all()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users

def update_user(id, username):
    user = get_user(id)
    if user:
        user.username = username
        db.session.add(user)
        return db.session.commit()
    return None

def create_job(title,description,manager_id,expected_qualifications):
    job = Job(title=title,description=description,manager_id=manager_id,expected_qualifications=expected_qualifications)
    db.session.add(job)
    db.session.commit()
    return job

def get_all_jobs():
    return Job.query.all()

def apply_to_job(job_id,user_id,qualifications):
    applicant = Applicant(user_id=user_id, job_id=job_id, qualifications=qualifications)
    db.session.add(applicant)
    db.session.commit()
    return applicant

def login(username,password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return create_access_token(identity=user.id)
    return None
