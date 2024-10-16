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
    update_user
)

LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):

    def test_new_user(self):
        user = User(username="bob", password="bobpass", 
                    first_name="Bob", last_name="Smith", email="bob@example.com")
        self.assertEqual(user.username, "bob")
        self.assertEqual(user.first_name, "Bob")
        self.assertEqual(user.last_name, "Smith")
        self.assertEqual(user.email, "bob@example.com")
        self.assertNotEqual(user.password, "bobpass")  

    # pure function no side effects or integrations called
    def test_get_user_json(self):
        user = User(username="alice", password="alicepass", 
                    first_name="Alice", last_name="Johnson", email="alice@example.com")
        expected_json = {
            'id': None, 
            'username': 'alice', 
            'first_name': 'Alice', 
            'last_name': 'Johnson', 
            'email': 'alice@example.com'
        }
        self.assertDictEqual(user.get_json(), expected_json)

    
    def test_hashed_password(self):
        password = "mypass"
        user = User(username="bob", password=password, first_name="Bob", last_name="Smith", email="bob@example.com")
        self.assertNotEqual(user.password,password)
        self.assertTrue(user.check_password(password))


    def test_check_password(self):
        user = User(username="dana", password="securepass", 
                    first_name="Dana", last_name="White", email="dana@example.com")
        self.assertTrue(user.check_password("securepass"))
        self.assertFalse(user.check_password("wrongpass"))

'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'})
    with app.app_context():
        create_db(app)  # Initialize the test database
        yield app.test_client()  # Provide test client
        db.drop_all()  

class UserIntegrationTests(unittest.TestCase):

    def test_user_creation(self):
        """Test creating a user via the controller."""
        user = create_user("john_doe", "password", "John", "Doe", "john@example.com")
        self.assertIsNotNone(user)
        self.assertEqual(user.username, "john_doe")

    def test_login(self,client):
        create_user("john_doe", "password", "John", "Doe", "john@example.com")
        data = {"username": "john_doe", "password": "password"}
        response = self.client.post("/api/login", json=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.get_json())

    def test_invalid_login(self,client):
        data = {"username": "wronguser", "password": "wrongpass"}
        response = self.client.post("/api/login", json=data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.get_json().get("message"), "bad username or password given")

if __name__ == "__main__":
    unittest.main()