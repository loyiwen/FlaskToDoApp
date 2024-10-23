import unittest
from app import app

class FlaskTest(unittest.TestCase):
    def setUp(self):
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

if __name__ == '__main__':
    unittest.main()