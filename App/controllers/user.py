from App.models import User,Job,Applicant
from App.database import db
from flask_jwt_extended import create_access_token
from flask_jwt_extended import unset_jwt_cookies


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

def login(username,password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return create_access_token(identity=user.id)
    return None

def create_job(title,description,manager_id,expected_qualifications):
    job = Job(title=title,description=description,manager_id=manager_id,expected_qualifications=expected_qualifications)
    db.session.add(job)
    db.session.commit()
    return job

def get_all_jobs():
    return Job.query.all()

def view_job_details(job_id):
    return Job.query.get(job_id)

def filter_job_title(title):
    return Job.query.filter(Job.title.contains(title)).all()

def close_job(job_id):
    job = Job.query.get(job_id)
    if job:
        job.status = 'closed'
        db.session.commit()
    return job

def apply_to_job(job_id,user_id,qualifications,status,cover_letter):
    applicant = Applicant(user_id=user_id, job_id=job_id, qualifications=qualifications, status = status, cover_letter = cover_letter)
    db.session.add(applicant)
    db.session.commit()
    return applicant

def update_job(job_id,title,description,expected_qualifications):
    job = job.query.get(job_id)
    if job:
        job.title = title
        job.desctription = description
        job.expected_qualifications = expected_qualifications
        db.session.commit()
        return job
    return None

def detele_job(job_id):
    job = job.query.get(job_id)
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
