from App.database import db

class Student(db.Model):
    studentID = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(50), nullable=False)
    lastName = db.Column(db.String(50), nullable=False)
    programme = db.Column(db.String(100), nullable=False)
    faculty = db.Column(db.String(100), nullable=False)

    # Relationship
    reviews = db.relationship('Review', back_populates='student') # a student can have mutliple reviews

    def __init__(self, studentID, firstName, lastName, programme, faculty):
        self.studentID = studentID
        self.firstName = firstName
        self.lastName = lastName
        self.programme = programme
        self.faculty = faculty

    def get_json(self):
        return {
            'studentID': self.studentID,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'programme': self.programme,
            'faculty': self.faculty
        }
