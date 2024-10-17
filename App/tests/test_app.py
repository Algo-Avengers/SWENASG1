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
        student = add_student("Jake Blue", "12345", "Computer Science", "DCIT")
        assert student.id == "12345"
        assert student.name == "Jake Blue"
        assert student.programme == "Computer Science"
        assert student.department == "DCIT"

    def test_search_student(self):
        student = add_student("Jake Blue", "12345", "Computer Science", "DCIT")
        search_result = search_student("12345")
        assert search_result is not None
        assert search_result.id == "12345"
        assert search_result.name == "Jake Blue"

    def test_add_review(self):
        student = add_student("Jake Blue", "12345", "Computer Science", "DCIT")
        review = add_review("12345", "0001", "Positive", "COMP 1601", "Excellent Conduct")
        assert review.studentid == "12345"
        assert review.staffid == "0001"
        assert review.type == "Positive"
        assert review.course == "COMP 1601"
        assert review.comment == "Excellent Conduct"

    def test_view_reviews(self):
        student = add_student("Jake Blue", "12345", "Computer Science", "DCIT")
        add_review("12345", "0001", "Positive", "COMP 1601", "Excellent Conduct")
        reviews_list = view_student_reviews("12345")
        assert reviews_list is not None
        assert len(reviews_list) > 0
        assert reviews_list[0].student_id == "12345"

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
        student = add_student("John Doe", "12345")
        retrieved_student = get_user(student.id)
        assert retrieved_student is not None
        assert retrieved_student.name == "John Doe"
        assert retrieved_student.student_id == "12345"

    def test_add_review(self):
        student = add_student("Jane Doe", "54321")
        add_review(student.id, "Good performance", 5)
        reviews = view_student_reviews(student.id)
        assert len(reviews) == 1
        assert reviews[0].content == "Good performance"
        assert reviews[0].rating == 5

    def test_search_student(self):
        student = add_student("Alice", "67890")
        searched_student = search_student("67890")
        assert searched_student is not None
        assert searched_student.name == "Alice"
        assert searched_student.student_id == "67890"

    def test_view_student_reviews(self):
        student = add_student("Bob", "09876")
        add_review(student.id, "Excellent", 5)
        add_review(student.id, "Needs improvement", 3)
        reviews = view_student_reviews(student.id)
        assert len(reviews) == 2
        assert reviews[0].content == "Excellent"
        assert reviews[0].rating == 5
        assert reviews[1].content == "Needs improvement"
        assert reviews[1].rating == 3
        

