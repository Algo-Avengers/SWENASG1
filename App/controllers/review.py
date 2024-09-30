from App.models import Review
from App.database import db

def add_review(reviewID, studentID, staffID, reviewType, comment):
    
    new_review = Review(
        reviewID=reviewID, 
        studentID=studentID,
        staffID=staffID,
        reviewType=reviewType,
        #date=date,
        comment=comment
    )
    db.session.add(new_review)
    db.session.commit()
    return new_review

def view_reviews(student_id: int):
    reviews = Review.query.filter_by(studentID=student_id).all()
    if reviews:
        return reviews
    return None