from App.models import Review
from App.database import db

def add_review(student_id, staff_id, review_type, course, comment):
    student = student.query.get(student_id)
    staff = staff.query.get(staff_id)

    if not student:
        return {"message": "Student not found."}
    if not staff:
        return {"message": "Staff not found."}

    new_review = Review(studentID=student_id, staffID=staff_id, reviewType=review_type, course=course, comment=comment)
    db.session.add(new_review)
    db.session.commit()
    return {"message": "Review added successfully"}

def view_student_reviews(student_id):
    student = student.query.get(student_id)
    if not student:
        return {"message": "Student not found."}

    reviews = Review.query.filter_by(studentID=student_id).all()
    if not reviews:
        return {"message": "No reviews found for this student."}

    review_list = [review_to_json(review) for review in reviews]
    return {"reviews": review_list}

def review_to_json(review):
    return {
        "id": review.reviewID,
        "student_id": review.studentID,
        "staff_id": review.staffID,
        "type": review.reviewType,
        "course": review.course,
        "comment": review.comment,
        "timestamp": review.timestamp
    }