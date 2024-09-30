import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User
from App.main import create_app
from App.controllers import (
    create_user, get_all_users_json, get_all_users, initialize,
    add_student, view_reviews, 
    add_review, search_student, get_all_students
)

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

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
Staff Commands
'''

# group for staff commands: flask staff <command>

staff_cli = AppGroup('staff', help='Staff object commands')

#Command to add students - Add Student
# flask staff add 123 Jake Blue "Computer Science" "FST"
@staff_cli.command("add", help="Add a student")
@click.argument("student_id", type=int)
@click.argument("first_name", type=str)
@click.argument("last_name", type=str)
@click.argument("programme", type=str)
@click.argument("faculty", type=str)
def add_student_command(student_id, first_name, last_name, programme, faculty):
    add_student(student_id, first_name, last_name, programme, faculty)
    print(f'Student {first_name} {last_name} added!')

#command to search for a student using student ID - Search Student
#Returns student name and their reviews
# flask staff search 123
@staff_cli.command("search", help="Search a student by ID and Name")
@click.argument("student_id", type=int)
def search_student_command(student_id):
    student = search_student(student_id)
    if student:
        print(f"Student found: {student.firstName} {student.lastName}, ID: {student.studentID}")
        reviews = student.reviews
        if reviews:
            print("Reviews:")
            for review in reviews:
                print(f"- {review.reviewType}: {review.comment} (Staff ID: {review.staffID})")
        else:
            print("No reviews found for this student.")
    else:
        print(f"No student found with ID {student_id} and name {student.firstName} {student.lastName}.")

#extra command that lists all students added and their information
# flask staff listStudents
@staff_cli.command("listStudents", help="List all students in the system")
def list_students_command():
    students = get_all_students()
    if students:
        for student in students:
            print(f"Student ID: {student.studentID}")
            print(f"Name: {student.firstName} {student.lastName}")
            print(f"Programme: {student.programme}")
            print(f"Faculty: {student.faculty}")
            print("-----------")  # Separator between students
    else:
        print("No students found in the system.")

app.cli.add_command(staff_cli) # adds staff group to the cli

'''
Review Commands
'''
# group for review commands: flask review <command>

review_cli = AppGroup('review', help='Review related commands')

# command that adds/creates a new review - Review Student
# flask review create 100 123 001 "Positive" "Good at participation."
@review_cli.command("create", help="Create a new review")
@click.argument("review_id", type=int)
@click.argument("student_id", type=int)
@click.argument("staff_id", type=int)
@click.argument("review_type", type=str)
@click.argument("comment", type=str)
def create_review_command(review_id, student_id, staff_id, review_type, comment):
    review = add_review(review_id, student_id, staff_id, review_type, comment)
    if review:
        print(f"Review for student {student_id} created!")
    else:
        print("Failed to create review.")

#command that views all reviews for a specific student - View Student Reviews
# flask review viewreviews 123
@review_cli.command("viewreviews", help="View all reviews for a student")
@click.argument("student_id", type=int)
def view_reviews_command(student_id):
    reviews = view_reviews(student_id)
    if reviews:
        for review in reviews:
            print(f"Review ID: {review.reviewID}")
            print(f"Staff ID: {review.staffID}")
            print(f"Review Type: {review.reviewType}")
            print(f"Comment: {review.comment}")
            print("-----------")  # Separator between reviews
    else:
        print(f"No reviews found for student with ID {student_id}.")

app.cli.add_command(review_cli) #adds review group to the cli


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
    

app.cli.add_command(test)