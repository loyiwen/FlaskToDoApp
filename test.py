import unittest
from app import app, db
from models import Assessment
from config import TestingConfig


class FlaskTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up testing environment with TestingConfig
        app.config.from_object(TestingConfig)
        app.config['TESTING'] = True

        # Initialise and create tables
        with app.app_context():
            db.create_all()
            print("Tables created in setUpClass")

    @classmethod
    def tearDownClass(cls):
        # Clean up tables after all tests in this class are run
        with app.app_context():
            db.session.remove()
            db.drop_all()
            print("Tables dropped in tearDownClass")

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


class DatabaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up the testing environment with TestingConfig
        app.config.from_object(TestingConfig)
        with app.app_context():
            db.create_all()
            print("Database tables created in DatabaseTest")

    @classmethod
    def tearDownClass(cls):
        # Clean up tables after all tests in this class are run
        with app.app_context():
            db.session.remove()
            db.drop_all()
            print("Database tables dropped in DatabaseTest")

    def setUp(self):
        # Push application context and create a test client for each test method
        self.app_context = app.app_context()
        self.app_context.push()
        self.app = app.test_client()
 
    def tearDown(self):
        # Pop application context after each test method
        self.app_context.pop()

    def test_create_assessment_form_submission(self):
        # Simulate valid form submission via POST request
        response = self.app.post('/create', data={
            'title': 'Test Assessment',
            'module_code': 'COMP2011',
            'deadline': '2024-10-25',
            'description': 'test description',
            'is_complete': False
        }, follow_redirects=True)

        # Check if form submission was successful (status code 200)
        self.assertEqual(response.status_code, 200)

        # Query database to check if assessment was added
        assessment = Assessment.query.filter_by(title='Test Assessment').first()
        self.assertIsNotNone(assessment)
        self.assertEqual(assessment.module_code, 'COMP2011')
        self.assertEqual(assessment.deadline.strftime('%Y-%m-%d'), '2024-10-25')


    def test_invalid_assessment_submission(self):
        # Simulate invalid form submission with missing required fields
        response = self.app.post('/create', data={
            'title': '',
            'module_code': '',
            'deadline': '',
            'description': ''
        }, follow_redirects=True)

        # Check that response contains error message (form should not submit)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'This field is required', response.data)


if __name__ == '__main__':
    unittest.main()