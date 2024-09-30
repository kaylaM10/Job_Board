import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User,Job,Applicants
from App.main import create_app
from App.controllers import ( 
    create_user, 
    get_all_users_json, 
    get_all_users, 
    initialize,
    create_job,
    apply_to_job 
)


# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

def create_tables():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli

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

@click.command('create-job')
@click.argument('title')
@click.argument('description')
@click.argument('manager_id')
@click.argument('expected_qualifications')
def create_job_command(title,description,manager_id,expected_qualifications):
    create_job(title, description, manager_id, expected_qualifications)
    click.echo(f'Job {title} created!')

@click.command('apply-job')
@click.argument('job_id')
@click.argument('user_id')
@click.argument('qualifications')
def apply_to_job_command(job_id,user_id,qualifications):
    apply_to_job(job_id,user_id,qualifications)
    click.echo(f'User {user_id} applied to job{job_id}!')

app.cli.add_command(test)
app.cli.add_command(create_job_command)
app.cli.add_command(apply_to_job_command)