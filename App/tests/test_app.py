import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import User
from App.controllers import (
    create_user,
    get_all_users_json,
    login,
    get_user,
    get_user_by_username,
    update_user,
    add_student,
    search_student,
    add_review,
    view_student_reviews
)


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):

    def test_new_user(self):
        user = User("bob", "bobpass")
        assert user.username == "bob"

    # pure function no side effects or integrations called
    def test_get_json(self):
        user = User("bob", "bobpass")
        user_json = user.get_json()
        self.assertDictEqual(user_json, {"id":None, "username":"bob"})
    
    def test_hashed_password(self):
        password = "mypass"
        hashed = generate_password_hash(password, method='sha256')
        user = User("bob", password)
        assert user.password != password

    def test_check_password(self):
        password = "mypass"
        user = User("bob", password)
        assert user.check_password(password)

    def test_add_student(self):
        student = add_student(12345, "Jake", "Blue", "Computer Science", "FST")
        assert student['id'] == 12345
        assert student['first_name'] == "Jake"
        assert student['last_name'] == "Blue"
        assert student['programme'] == "Computer Science"
        assert student['faculty'] == "FST"

    def test_add_review(self):
        student = add_student(12345, "Jake", "Blue", "Computer Science", "FST")
        review = add_review(12345, 1, "Positive", "COMP 1601", "Excellent Conduct")
        assert review['student_id'] == 12345  
        assert review['staff_id'] == 1
        assert review['type'] == "Positive"
        assert review['course'] == "COMP 1601"
        assert review['comment'] == "Excellent Conduct"

    def test_search_student(self):
        student = add_student(12345, "Jake", "Blue", "Computer Science", "FST")
        search_result = search_student(12345)
        assert search_result is not None
        assert search_result['id'] == 12345  
        assert search_result['first_name'] == "Jake"

    def test_view_reviews(self):
        student = add_student(12345, "Jake", "Blue", "Computer Science", "FST")
        add_review(12345, 1, "Positive", "COMP 1601", "Excellent Conduct")
        reviews_list = view_student_reviews(12345)
        assert reviews_list is not None
        assert len(reviews_list) > 0
        assert reviews_list[0]['student_id'] == 12345 

'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()


def test_authenticate():
    user = create_user("bob", "bobpass")
    assert login("bob", "bobpass") != None

class UsersIntegrationTests(unittest.TestCase):

    def test_create_user(self):
        user = create_user("rick", "bobpass")
        assert user.username == "rick"

    def test_get_all_users_json(self):
        users_json = get_all_users_json()
        self.assertListEqual([{"id":1, "username":"bob"}, {"id":2, "username":"rick"}], users_json)

    # Tests data changes in the database
    def test_update_user(self):
        update_user(1, "ronnie")
        user = get_user(1)
        assert user.username == "ronnie"
    
    # creates an empty database for the test and deletes it after the test
    def setUp(self):
        self.app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
        self.client = self.app.test_client()
        create_db()

    def test_login(self):
        staff = create_user("staff", "staffpass", is_staff=True)
        assert login("staff", "staffpass") != None
        user = get_user_by_username("staff")
        assert user is not None
        assert user.username == "staff"
        assert user.is_staff == True

    def test_add_student(self):
        student = add_student(12345, "John", "Doe", "Computer Science", "FST")
        retrieved_student = search_student(12345)  # Use search_student to verify
        assert retrieved_student is not None
        assert retrieved_student.first_name == "John"
        assert retrieved_student.last_name == "Doe"
        assert retrieved_student.id == 12345

    def test_add_review(self):
        student = add_student("Jane Doe", "54321")
        add_review(student.id, "Good performance", 5)
        reviews = view_student_reviews(student.id)
        assert len(reviews) == 1
        assert reviews['reviews'][0]['comment'] == "Great job on the project!"  # Ensure you're checking comment
        
    def test_search_student(self):
            student = add_student(67890, "Alice", "Smith", "Mathematics", "FST")
            searched_student = search_student(67890)
            assert searched_student is not None
            assert searched_student.first_name == "Alice"
            assert searched_student.last_name == "Smith"
            assert searched_student.id == 67890

    def test_view_student_reviews(self):
        student = add_student("Bob", "09876")
        add_review(student.id, "1000", "Excellent", "COMP 3613", "Excellent performance.")
        add_review(student.id, "1000", "Needs improvement", "COMP 3613", "Could do better next time.")
        reviews = view_student_reviews(student.id)
        assert len(reviews) == 2
        assert reviews['reviews'][0]['comment'] == "Excellent performance."
        assert reviews['reviews'][1]['comment'] == "Could do better next time."
        

