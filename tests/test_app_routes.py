import unittest
from app import app, db
from config import TestingConfig

class AppRoutesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up testing environment with TestingConfig
        app.config.from_object(TestingConfig)
        app.config['TESTING'] = True

        # Initialise and create tables for testing
        with app.app_context():
            db.create_all()
            print("Database tables created in AppRoutesTest")

    @classmethod
    def tearDownClass(cls):
        # Drop all tables after all tests in this class are run
        with app.app_context():
            db.session.remove()
            db.drop_all()
            print("Database tables dropped in AppRoutesTest")

    def setUp(self):
        # Set up a test client for each test method
        self.app = app.test_client()

    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'All Assessments', response.data)

    def test_create_page(self):
        response = self.app.get('/create')
        self.assertIn(b'<input id="title"', response.data)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
