import unittest
from app import app, db
from models import Assessment

class FormValidationTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

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
