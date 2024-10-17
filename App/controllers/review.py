from App.models import Review
from App.database import db

def add_review(student_id, staff_id, review_type, course, comment):
    student = student.query.get(student_id)
    staff = staff.query.get(staff_id)

    if not student:
        return {"message": "Student not found."}
    if not staff:
        return {"message": "Staff not found."}

    new_review = Review(student_id=student_id, staff_id=staff_id, type=review_type, course=course, comment=comment)
    db.session.add(new_review)
    db.session.commit()
    return {"message": f"Review added successfully"}

def view_student_reviews(student_id):
    student = student.query.get(student_id)
    if not student:
        return {"message": "Student not found."}

    reviews = Review.query.filter_by(student_id=student_id).all()
    if not reviews:
        return {"message": "No reviews found for this student."}

    review_list = [review_to_json(review) for review in reviews]
    return {"reviews": review_list}

def review_to_json(review):
    return {
        "id": review.id,
        "student_id": review.student_id,
        "staff_id": review.staff_id,
        "type": review.type,
        "course": review.course,
        "comment": review.comment,
        "timestamp": review.timestamp
    }