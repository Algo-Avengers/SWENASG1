from App.models import Student
from App.database import db


def search_student(student_id):                                 
    student = Student.query.filter_by(studentID=student_id).first()
    if student:
        return student.get_json()
    else:
        return {"message": "Student doesn't exist."}


def add_student(student_id, first_name, last_name, programme, faculty):
    student = Student.query.filter_by(studentID=student_id).first()
    if student:
        return {"message": "Student already exists."}

    new_student = Student(studentID=student_id, firstName=first_name, lastName=last_name, programme=programme, faculty=faculty)
    db.session.add(new_student)
    db.session.commit()

    return {"message": f"Student {first_name} {last_name} added successfully."}

def toJSON(student):
    return {
        "studentID": student.studentID,
        "firstName": student.firstName,
        "lastName": student.lastName,
        "programme": student.programme,
        "faculty": student.faculty
    }

def get_all_students():
    students = Student.query.all() 
    return [toJSON(student) for student in students]
