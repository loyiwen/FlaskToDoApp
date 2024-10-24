from app import app
from models import db, Assessment
from config import TestingConfig
import unittest

# Test routes
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
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Create Assessment', response.data)


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


    def test_create_assessment(self):    
         # Create new assessment
        new_assessment = Assessment(
            title="Test Assessment",
            module_code="COMP2011",
            deadline="2024-10-25",
            description="test description",
            is_complete=False
        )

        db.session.add(new_assessment)
        db.session.commit()

        # Query assessment from database
        assessment = Assessment.query.filter_by(title="Test Assessment").first()
        self.assertIsNotNone(assessment)
        self.assertEqual(assessment.module_code, "COMP2011")

if __name__ == '__main__':
    unittest.main()