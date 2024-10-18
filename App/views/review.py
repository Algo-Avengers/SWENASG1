from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from App.controllers.review import review_to_json
from App.controllers import review, student
from App.database import db
from App.models import Review 



review_views = Blueprint('review_views', __name__)

@review_views.route('/api/review', methods=['POST'])
@jwt_required()
def create_review():
    data = request.json
    staffID = get_jwt_identity()
    studentID = data.get('studentID')
    reviewType = data.get('reviewType')
    comment = data.get('comment', '')
    course = data.get('course') 

    if not studentID or not reviewType:
        return jsonify({"error": "Student ID and review type are required"}), 400
    
    new_review = Review(  
        studentID=studentID,
        staffID=staffID,
        reviewType=reviewType,
        comment=comment,
        course=course
    )

    db.session.add(new_review)
    db.session.commit()
    
    return jsonify(review_to_json(new_review)), 201

@review_views.route('/api/review/student/<int:studentID>', methods=['GET'])
@jwt_required()
def get_student_reviews(studentID):
    reviews = Review.query.filter_by(studentID=studentID).all()
    if not reviews:
        return jsonify({"error": "No reviews found for this student"}), 404
    reviews_list = [review_to_json(review) for review in reviews]
    return jsonify({"reviews": reviews_list}), 200

@review_views.route('/api/review/<int:reviewID>', methods=['GET'])
@jwt_required()
def get_review(reviewID):
    review = Review.query.get(reviewID)
    if not review:
        return jsonify({"error": "Review not found"}), 404
    return jsonify(review_to_json(review)), 200

@review_views.route('/api/review/<int:reviewID>', methods=['PUT'])
@jwt_required()
def update_review(reviewID):
    data = request.json
    reviewType = data.get('reviewType')
    comment = data.get('comment')
    if not reviewType:
        return jsonify({"error": "Review type is required"}), 400
    review = Review.query.get(reviewID)
    if not review:
        return jsonify({"error": "Review not found"}), 404
    review.reviewType = reviewType
    review.comment = comment
    db.session.commit()
    return jsonify(review_to_json(review)), 200
