import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup
from werkzeug.security import generate_password_hash

from App.database import db, get_migrate
from App.models import User,Job,Applicant
from App.main import create_app
from App.controllers import ( 
    create_user, 
    get_all_users_json, 
    get_all_users, 
    initialize,
    create_job,
    apply_to_job 
)


# This commands file allows you to create convenient CLI commands for testing controllers

# Create the Flask app instance
app = create_app()
migrate = get_migrate(app)

# Function to create tables
def create_tables():
    db.create_all()

# Command to create and initialize the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('Database initialized')

'''
User Commands
'''

# Commands can be organized using groups
user_cli = AppGroup('user', help='User object commands')

@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
@click.argument("first_name", default="Rob")
@click.argument("last_name", default="Robinson")
@click.argument("email", default="rob@example.com")
def create_user_command(username, password, first_name, last_name, email):
    try:
        create_user(username, password, first_name, last_name, email)
        print(f'User {username} created with first name {first_name}, last name {last_name}, email {email}!')
    except ValueError as e:
        print(e)  # Print if the email is already taken
    except Exception as e:
        print(f'Error creating user: {e}')  # Print any other errors

@user_cli.command("list", help="Lists users in the database")
def list_users_command():
    try:
        users = User.query.all()
        if not users:
            print("No users found.")
            return
        for user in users:
            print(f'Username: {user.username}, Email: {user.email}')
    except Exception as e:
        print(f'Error fetching users: {e}')  # Print error if there's an issue

app.cli.add_command(user_cli)  # Add the group to the CLI

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands')

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))

# Command to create a job
@click.command('create-job')
@click.argument('title')
@click.argument('description')
@click.argument('manager_id')
@click.argument('expected_qualifications')
def create_job_command(title, description, manager_id, expected_qualifications):
    create_job(title, description, manager_id, expected_qualifications)
    click.echo(f'Job {title} created!')

# Command to apply for a job
@click.command('apply-job')
@click.argument('job_id')
@click.argument('user_id')
@click.argument('qualifications')
def apply_to_job_command(job_id, user_id, qualifications):
    apply_to_job(job_id, user_id, qualifications)
    click.echo(f'User {user_id} applied to job {job_id}!')

# Add the test and job commands to the app CLI
app.cli.add_command(test)
app.cli.add_command(create_job_command)
app.cli.add_command(apply_to_job_command)

if __name__ == "__main__":
    app.run(debug=True)