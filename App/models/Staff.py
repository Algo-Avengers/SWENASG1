from App.database import db

class Staff(db.Model):
    staffID = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(50), nullable=False)
    lastName = db.Column(db.String(50), nullable=False)
    faculty = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)

     # Relationship
    reviews = db.relationship('Review', back_populates='staff') # staff can create multiple reviews

    def __init__(self, staffID, firstName, lastName, faculty, department):
        self.staffID = staffID
        self.firstName = firstName
        self.lastName = lastName
        self.faculty = faculty
        self.department = department

    def get_json(self):
        return {
            'staffID': self.staffID,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'faculty': self.faculty,
            'department': self.department
        }
