import unittest
from app import app, db
from models import Assessment
from config import TestingConfig
from datetime import datetime

class DatabaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up testing environment with TestingConfig
        app.config.from_object(TestingConfig)
        app.config['TESTING'] = True

        # Create database tables for testing
        with app.app_context():
            db.create_all()
            print("Database tables created in DatabaseTest")

    @classmethod
    def tearDownClass(cls):
        # Drop all tables after all tests in this class are run
        with app.app_context():
            db.session.remove()
            db.drop_all()
            print("Database tables dropped in DatabaseTest")

    def setUp(self):
        # Create new test client and application context for each test method
        self.app_context = app.app_context()
        self.app_context.push()
        self.app = app.test_client()
 
    def tearDown(self):
        # Remove all entries from the database and pop application context
        with app.app_context():
            db.session.query(Assessment).delete()
            db.session.commit()
        self.app_context.pop()

if __name__ == '__main__':
    unittest.main()