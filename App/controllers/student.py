from App.models import Student
from App.database import db


def search_student(student_id):                                 
    student = Student.query.filter_by(id=student_id).first()
    if student:
        return student.get_json()
    else:
        return {"message": "Student doesn't exist."}


def add_student(student_id, student_name):
    student = Student.query.filter_by(id=student_id).first()
    if student:
        return {"message": "Student already exists."}

    new_student = Student(id=student_id, name=student_name)
    db.session.add(new_student)
    db.session.commit()

    return {"message": f"Student {student_name} added successfully."}

def toJSON(student):
    return {
        "id": student.id,
        "name": student.name
    }

def get_all_students():
    students = Student.query.all()  # Fetch all students from the database
    return students
