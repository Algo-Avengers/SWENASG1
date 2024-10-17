from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from App.controllers.review import review_to_json
from App.controllers import review, student
from App.database import db

review_views = Blueprint('review_views', __name__)

@review_views.route('/api/review', methods=['POST'])
@jwt_required()
def create_review():
    data = request.json
    staff_id = get_jwt_identity()
    student_id = data.get('student_id')
    review_type = data.get('type')
    course = data.get('course')
    comment = data.get('comment')
    if not student_id or not review_type or not course or not comment:
        return jsonify({"error": "Student ID, type, course, and comment are required"}), 400
    new_review = review(
        student_id=student_id,
        staff_id=staff_id,
        type=review_type,
        course=course,
        comment=comment
    )
    db.session.add(new_review)
    db.session.commit()
    return jsonify(review_to_json(new_review)), 201

@review_views.route('/api/review/student/<int:student_id>', methods=['GET'])
@jwt_required()
def get_student_reviews(student_id):
    reviews = review.query.filter_by(student_id=student_id).all()
    if not reviews:
        return jsonify({"error": "No reviews found for this student"}), 404
    reviews_list = [review_to_json(review) for review in reviews]
    return jsonify({"reviews": reviews_list}), 200

@review_views.route('/api/review/<int:id>', methods=['GET'])
@jwt_required()
def get_review(id):
    review = review.query.get(id)
    if not review:
        return jsonify({"error": "Review not found"}), 404
    return jsonify(review_to_json(review)), 200

@review_views.route('/api/review/<int:id>', methods=['PUT'])
@jwt_required()
def update_review(id):
    data = request.json
    review_type = data.get('type')
    course = data.get('course')
    comment = data.get('comment')
    if not review_type or not course or not comment:
        return jsonify({"error": "Type, course, and comment are required"}), 400
    review = review.query.get(id)
    if not review:
        return jsonify({"error": "Review not found"}), 404
    review.type = review_type
    review.course = course
    review.comment = comment
    db.session.commit()
    return jsonify(review_to_json(review)), 200

@review_views.route('/api/review/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_review(id):
    review = review.query.get(id)
    if not review:
        return jsonify({"error": "Review not found"}), 404
    db.session.delete(review)
    db.session.commit()
    return jsonify({"message": "Review deleted"}), 200