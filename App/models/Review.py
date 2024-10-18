from App.database import db

class Review(db.Model):
    reviewID = db.Column(db.Integer, primary_key=True)
    studentID = db.Column(db.Integer, db.ForeignKey('student.studentID'), nullable=False)
    staffID = db.Column(db.Integer, db.ForeignKey('staff.staffID'), nullable=False)
    reviewType = db.Column(db.String(50), nullable=False)
    comment = db.Column(db.String(255), nullable=True)
    course = db.Column(db.String(100), nullable=False)

    # Relationships
    student = db.relationship('Student', back_populates='reviews') 
    staff = db.relationship('Staff', back_populates='reviews') 
    def __init__(self, studentID, staffID, reviewType, comment, course):
        self.studentID = studentID
        self.staffID = staffID
        self.reviewType = reviewType
        self.comment = comment
        self.course = course 

    def get_json(self):
        return {
            'reviewID': self.reviewID,
            'studentID': self.studentID,
            'staffID': self.staffID,
            'reviewType': self.reviewType,
            'comment': self.comment,
            'course': self.course
        }
