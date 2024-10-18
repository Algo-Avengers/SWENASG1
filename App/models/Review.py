from App.database import db

class Review(db.Model):
    reviewID = db.Column(db.Integer, primary_key=True)
    studentID = db.Column(db.Integer, db.ForeignKey('student.studentID'), nullable=False)
    staffID = db.Column(db.Integer, db.ForeignKey('staff.staffID'), nullable=False)
    reviewType = db.Column(db.String(50), nullable=False)
    comment = db.Column(db.String(255), nullable=True)

    # Relationships
    student = db.relationship('Student', back_populates='reviews') # Each review belongs to one student.
    staff = db.relationship('Staff', back_populates='reviews') # Each student can have multiple reviews from different staff members.
    def __init__(self, reviewID, studentID, staffID, reviewType, comment):
        self.reviewID = reviewID
        self.studentID = studentID
        self.staffID = staffID
        self.reviewType = reviewType
        self.comment = comment

    def get_json(self):
        return {
            'reviewID': self.reviewID,
            'studentID': self.studentID,
            'staffID': self.staffID,
            'reviewType': self.reviewType,
            #'date': str(self.date),
            'comment': self.comment
        }
