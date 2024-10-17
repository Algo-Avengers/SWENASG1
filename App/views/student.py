from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from App.controllers import student
from App.database import db

student_views = Blueprint('student_views', __name__)

@student_views.route('/api/student/<int:id>', methods=['GET'])
@jwt_required()
def get_student(id):
    student = student.query.get(id)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    return jsonify(student.to_dict()), 200

@student_views.route('/api/student', methods=['GET'])
@jwt_required()
def get_all_students():
    students = student.query.all()
    return jsonify([student.to_dict() for student in students]), 200

@student_views.route('/api/student', methods=['POST'])
@jwt_required()
def create_student():
    data = request.json
    student_id = data.get('id')
    student_name = data.get('name')
    if not student_id or not student_name:
        return jsonify({"error": "Student ID and name required"}), 400
    result = student.add_student(student_id, student_name)
    return jsonify(result), 201 if "successfully" in result["message"] else 400

@student_views.route('/api/student/<int:id>', methods=['PUT'])
@jwt_required()
def update_student(id):
    data = request.json
    name = data.get('name')
    if not name:
        return jsonify({"error": "Name required"}), 400
    student = student.query.get(id)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    student.name = name
    db.session.commit()
    return jsonify(student.to_dict()), 200

@student_views.route('/api/student/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_student(id):
    student = student.query.get(id)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    db.session.delete(student)
    db.session.commit()
    return jsonify({"message": "Student deleted"}), 200