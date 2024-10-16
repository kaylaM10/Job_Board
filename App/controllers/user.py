from App.models import User, Job, Applicant
from App.database import db
from flask_jwt_extended import create_access_token, unset_jwt_cookies

def create_user(username, password, first_name, last_name, email):
    newuser = User(username=username, password=password, first_name=first_name, last_name=last_name, email=email)
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
    return [user.get_json() for user in users] if users else []

def update_user(id, username):
    user = get_user(id)
    if user:
        user.username = username
        db.session.commit()
    return user

def login(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return create_access_token(identity=user.id)
    return None

def create_job(title, description, manager_id, expected_qualifications):
    job = Job(title=title, description=description, user_id=manager_id, expected_qualifications=expected_qualifications)
    db.session.add(job)
    db.session.commit()
    return job

def get_all_jobs():
    return Job.query.all()

def view_job_details(job_id):
    return Job.query.get(job_id)

def filter_job_title(title):
    return Job.query.filter(Job.title.contains(title)).all()

def apply_to_job(job_id, user_id, applicant_name, qualifications, status='applied', cover_letter=None):
    applicant = Applicant(
        user_id=user_id, 
        job_id=job_id, 
        applicant_name=applicant_name, 
        qualifications=qualifications, 
        status=status, 
        cover_letter=cover_letter
    )
    db.session.add(applicant)
    db.session.commit()
    return applicant

def update_job(job_id, title, description, expected_qualifications):
    job = Job.query.get(job_id)
    if job:
        job.title = title
        job.description = description
        job.expected_qualifications = expected_qualifications
        db.session.commit()
    return job

def delete_job(job_id):
    job = Job.query.get(job_id)
    if job:
        db.session.delete(job)
        db.session.commit()
        return True
    return False

def applications_by_user(user_id):
    return Applicant.query.filter_by(user_id=user_id).all()

def applications_by_job(job_id):
    return Applicant.query.filter_by(job_id=job_id).all()

def logout(response):
    unset_jwt_cookies(response)
    return response