import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
#        self.database_path = "postgres://postgres:postgres@127.0.0.1:5432/{}".format(self.database_name)
        self.database_path = "postgresql://postgres:postgres@127.0.0.1:5432/trivia_test"
      #  self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_questions(self):
        """Test getting all questions"""
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['questions']) > 0)


    def test_create_new_question_success(self):
        """Test creating a new question"""
        new_question_data = {
            'question': 'What is the capital of Greece?',
            'answer': 'Athens',
            'category': 3,
            'difficulty': 2
        }
        res = self.client().post('/questions', json=new_question_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsNotNone(data['created'])



    def test_get_questions_by_category_fail(self):
        """Test getting questions by a category that doesn't exist"""
        non_existent_category_id = 999
        res = self.client().get(f'/categories/{non_existent_category_id}/questions')

        self.assertEqual(res.status_code, 404)
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Not Found')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
