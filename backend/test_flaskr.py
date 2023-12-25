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
##GET '/api/v1.0/categories'  SUCCESS
    
    def test_get_categories_success(self):
        """Test getting all categories successfully"""
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['categories']) > 0)

##GET '/api/v1.0/categories'  FAIL 
    def test_get_categories_fail(self):
        """Test getting categories when none exist"""
        # Assuming there are no categories at the beginning
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['categories']), 0)

##GET '/api/v1.0/questions'  SUCCESS
    def test_get_questions_success(self):
        """Test getting all questions successfully"""
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['questions']) > 0)

##GET '/api/v1.0/questions'  FAIL 
    def test_get_questions_fail(self):
        """Test getting questions when none exist"""
        # Assuming there are no questions at the beginning
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['questions']), 0)
    
##POST '/api/v1.0/questions' SUCCESS
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
        
## POST '/api/v1.0/questions' FAIL
    def test_create_new_question_missing_data(self):
        """Test creating a new question with missing data"""
        new_question_data = {
            'answer': 'Athens',
            'category': 3,
            'difficulty': 2
        }
        res = self.client().post('/questions', json=new_question_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'Unprocessable')


    def test_create_new_question_invalid_category(self):
        """Test creating a new question with an invalid category"""
        new_question_data = {
            'question': 'What is the capital of Greece?',
            'answer': 'Athens',
            'category': 999,  # Invalid category ID
            'difficulty': 2
        }
        res = self.client().post('/questions', json=new_question_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'Unprocessable')

##DELETE '/api/v1.0/questions/<question_id>' SUCCESS
    def test_delete_question_success(self):
        """Test deleting a question successfully"""
        # Create a sample question for deletion
        sample_question = Question(
            question='Sample Question',
            answer='Sample Answer',
            category=1,
            difficulty=1
        )
        sample_question.insert()

        # Perform the delete request
        res = self.client().delete(f'/api/v1.0/questions/{sample_question.id}')
        data = json.loads(res.data)

        # Verify the response
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], sample_question.id)

## DELETE '/api/v1.0/questions/<question_id>'FAIL
    def test_delete_question_not_found(self):
        """Test attempting to delete a non-existing question"""
        non_existent_question_id = 999
        res = self.client().delete(f'/api/v1.0/questions/{non_existent_question_id}')
        data = json.loads(res.data)

        # Verify the response
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Not Found')

##POST '/api/v1.0/questions/search' SUCCESS
    def test_search_questions_success(self):
        """Test searching for questions with a specific term"""
        search_term = 'boxer'
        res = self.client().post('/api/v1.0/questions/search', json={'searchTerm': search_term})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['total_questions'], 2)
        self.assertEqual(len(data['questions']), 2)
        self.assertIsNotNone(data['questions'][0]['id'])
        self.assertIsNotNone(data['questions'][1]['id'])

##POST '/api/v1.0/questions/search' FAIL
    def test_search_questions_no_results(self):
        """Test searching for questions with a term that yields no results"""
        search_term = 'nonexistentterm'
        res = self.client().post('/api/v1.0/questions/search', json={'searchTerm': search_term})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['total_questions'], 0)
        self.assertEqual(len(data['questions']), 0)

## GET '/api/v1.0/categories/<category_id>/questions' SUCCESS
    def test_get_questions_by_category_success(self):
        """Test getting questions by category"""
        # Add a test category
        test_category = Category(type='History')
        test_category.insert()

        # Add test questions in the test category
        test_questions = [
            {'question': 'Question 1', 'answer': 'Answer 1', 'category': test_category.id, 'difficulty': 2},
            {'question': 'Question 2', 'answer': 'Answer 2', 'category': test_category.id, 'difficulty': 1},
        ]
        for question_data in test_questions:
            test_question = Question(**question_data)
            test_question.insert()

        # Make a request to get questions by the test category id
        res = self.client().get(f'/api/v1.0/categories/{test_category.id}/questions')
        data = json.loads(res.data)

        # Assert the response
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['current_category'], test_category.type)
        self.assertTrue(len(data['questions']) > 0)
        self.assertEqual(data['total_questions'], len(data['questions']))


## GET '/api/v1.0/categories/<category_id>/questions' FAIL
    def test_get_questions_by_category_fail(self):
        """Test getting questions by a non-existent category"""
        non_existent_category_id = 999
        res = self.client().get(f'/api/v1.0/categories/{non_existent_category_id}/questions')

        # Assert the response
        self.assertEqual(res.status_code, 404)
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Not Found')



## POST '/api/v1.0/quizzes'   SUCCESS
    def test_play_quiz_success(self):
        """Test playing quiz and getting a random question successfully"""
        category_id = 1
        previous_questions = [1, 2, 3]  # Assuming these are question IDs that were previously asked
        quiz_data = {
            'previous_questions': previous_questions,
            'category': category_id
        }
        res = self.client().post('/quizzes', json=quiz_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsNotNone(data['question'])
        self.assertIn('id', data['question'])
        self.assertIn('question', data['question'])
        self.assertIn('answer', data['question'])
        self.assertIn('category', data['question'])
        self.assertIn('difficulty', data['question'])

## POST '/api/v1.0/quizzes' FAIL
    def test_play_quiz_fail_no_data(self):
        """Test playing quiz without providing required data and expect failure"""
        res = self.client().post('/quizzes')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'Bad Request')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
