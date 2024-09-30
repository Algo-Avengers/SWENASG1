from App.models import Student, Review  # Import Staff, Student, and Review models
from App.database import db

def add_student(student_id, first_name, last_name, programme, faculty):
    # Checks if the student already exists
    existing_student = Student.query.get(student_id)
    if existing_student:
        return None  # The case where the student already exists
    
    new_student = Student(
        studentID=student_id,
        firstName=first_name,
        lastName=last_name,
        programme=programme,
        faculty=faculty
    )
    db.session.add(new_student)
    db.session.commit()
    return new_student

def search_student(student_id: int):
    student = Student.query.filter_by(studentID=student_id).first()
    if student:
        return student
    return None

def get_all_students():
    students = Student.query.all()  # Fetch all students from the database
    return students
