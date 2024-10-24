import unittest
from app import app
from models import db, Assessment
from config import TestingConfig


class FlaskTest(unittest.TestCase):
    def setUp(self):
        # Enable Flask's testing mode
        app.config['TESTING'] = True
        self.app = app.test_client()


    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Home Page', response.data)


    def test_create_page(self):
        response = self.app.get('/create')
        self.assertIn(b'<input id="title"', response.data)
        self.assertEqual(response.status_code, 200)


class DatabaseTest(unittest.TestCase):
    def setUp(self):
        app.config.from_object(TestingConfig)

        # Push an application context
        self.app_context = app.app_context()
        self.app_context.push()

        # Set up test client
        self.app = app.test_client()

        db.create_all()
    

    def tearDown(self):
        # Remove session and drop tables
        db.session.remove()
        db.drop_all()

        # Pop application context
        self.app_context.pop()


    def test_create_assessment_form_submission(self):
        # Simulate form submission via POST request
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
        # Simulate form submission with missing required fields
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