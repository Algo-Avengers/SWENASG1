from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from App.controllers import student
from App.database import db
from App.models import Student


student_views = Blueprint('student_views', __name__)

@student_views.route('/api/student/<int:id>', methods=['GET'])
@jwt_required()
def search_student(id):
    student = Student.query.get(id)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    return jsonify({
        "studentID": student.studentID,
        "firstName": student.firstName,
        "lastName": student.lastName,
        "programme": student.programme,
        "faculty": student.faculty
    }), 200

@student_views.route('/api/student', methods=['GET'])
@jwt_required()
def get_all_students():
    students = Student.query.all()
    
    return jsonify([{
        'studentID': student.studentID,
        'firstName': student.firstName,
        'lastName': student.lastName,
        'programme': student.programme,
        'faculty': student.faculty
    } for student in students]), 200

@student_views.route('/api/student', methods=['POST'])
@jwt_required()
def create_student():
    data = request.json
    student_id = data.get('studentID')
    first_name = data.get('firstName')
    last_name = data.get('lastName')
    programme = data.get('programme')
    faculty = data.get('faculty')
    if not student_id or not first_name or not last_name or not programme or not faculty:
        return jsonify({"error": "Student ID, first name, last name, programme, and faculty required"}), 400
    result = student.add_student(student_id, first_name, last_name, programme, faculty)
    return jsonify(result), 201 if "successfully" in result["message"] else 400

@student_views.route('/api/student/<int:id>', methods=['PUT'])
@jwt_required()
def update_student(id):
    data = request.json
    first_name = data.get('firstName')
    last_name = data.get('lastName')
    programme = data.get('programme')
    faculty = data.get('faculty')
    if not first_name or not last_name or not programme or not faculty:
        return jsonify({"error": "First name, last name, programme, and faculty required"}), 400
    student = Student.query.get(id)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    student.firstName = first_name
    student.lastName = last_name
    student.programme = programme
    student.faculty = faculty
    db.session.commit()
    return jsonify(student.to_dict()), 200
