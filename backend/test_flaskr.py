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
        self.database_path = "postgresql://{}:{}@{}/{}".format('student','student','localhost:5432', self.database_name)
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

    def test_endpoint_to_list_categories_should_return_valid_response(self):
        req = self.client().get("/api/v1/categories")
        data = json.loads(req.data)
        self.assertEqual(200,req.status_code)
        self.assertIn("categories",data)
        self.assertTrue(data["categories"])

    def test_get_questions_should_return_valid_response(self):
        req = self.client().get("/api/v1/questions?page=1")
        data = json.loads(req.data)
        self.assertEqual(200,req.status_code)
        self.assertTrue(data["questions"])
        self.assertGreaterEqual(data["total_questions"],1)
        self.assertTrue(data["categories"])
        self.assertTrue(data["currentCategory"])
    
    def test_delete_questions_shoud_be_permanent_to_db(self):
        print("This test may fail for a second test attempt")
        id = 10
        question_with_data  = Question.query.filter(Question.id==id).one_or_none()
        self.assertIsNotNone(question_with_data)
        req = self.client().delete(f"/api/v1/questions/{id}")
        data = json.loads(req.data)
        question  = Question.query.filter(Question.id==id).one_or_none()
        self.assertEqual(200,req.status_code)
        self.assertEqual(data["id"],id)
        self.assertIsNone(question)

    def test_delete_questions_shoud_not_succeed_for_inexistant_question(self):
        id = 1022
        req = self.client().delete(f"/api/v1/questions/{id}")
        data = json.loads(req.data)
        self.assertEqual(422,req.status_code)
    
    def test_add_new_question_should_check_required_datas(self):
        req = self.client().post("/api/v1/questions",json={
            "question": "Heres a new question string",
            "answer": "Heres a new answer string",
            "difficulty": 1,
        })
        data = json.loads(req.data)
        self.assertEqual(400,req.status_code)
        self.assertEqual("Some informations are missing, can't process your request",data["message"])

    def test_add_new_question_should_validate_json_datas(self):
        req = self.client().post("/api/v1/questions",json={
            "question": "Heres a new question string",
            "answer": 1,
            "difficulty": "Easy",
            "category" : 2
        })
        data = json.loads(req.data)
        self.assertEqual(400,req.status_code)
        self.assertEqual("Your datas seems to not be well formated, can't process your request",data["message"])
    
    def test_add_new_question_should_save_post(self):
        req = self.client().post("/api/v1/questions",json={
            "question": "Who is the president of Congo DR",
            "answer": "Felix Tshisekedi",
            "difficulty": 2,
            "category" : 5
        })
        data = json.loads(req.data)
        self.assertEqual(200,req.status_code)
        self.assertIn("id",data)
        id = data["id"]
        quest = Question.query.filter(Question.id==id).one_or_none()
        self.assertIsNotNone(quest)
    
    def test_search_question_should_appear_in_result(self):
        res = self.client().post('/api/v1/questions',json={"searchTerm":"What"})
        data = json.loads(res.data)
        self.assertEqual(200, res.status_code)
        self.assertTrue(data["questions"])
        self.assertIn("What",data["questions"][0]["question"])

            
    def test_search_question_should_be_case_insensitive(self):
        res = self.client().post('/api/v1/questions',json={"searchTerm":"wHAt"})
        data = json.loads(res.data)
        self.assertEqual(200, res.status_code)
        self.assertTrue(data["questions"])
        self.assertIn("What",data["questions"][0]["question"])

               
    def test_search_question_should_match_anysubstring(self):
        res = self.client().post('/api/v1/questions',json={"searchTerm":"hat"})
        data = json.loads(res.data)
        self.assertEqual(200, res.status_code)
        self.assertTrue(data["questions"])
        self.assertIn("What",data["questions"][0]["question"])

    
    def test_search_inexitant_title_should_return_empty(self):
        res = self.client().post('/api/v1/questions',json={"searchTerm":"ffadhlsjqpwirriirjfneewiq"})
        data = json.loads(res.data)
        self.assertEqual(200, res.status_code)
        self.assertFalse(data["questions"])

    def test_get_question_within_category(self):
        catID = 2
        res = self.client().get(f"/api/v1/categories/{catID}/questions")
        data = json.loads(res.data)
        self.assertEqual(200,res.status_code)
        questions_ob = [questions for questions in data["questions"]]
        questions_only=[]
        for quest in questions_ob:
            questions_only.append(quest["question"])
        self.assertEqual(200,res.status_code)
        self.assertIn("La Giaconda is better known as what?",questions_only)
        self.assertNotIn("What boxer's original name is Cassius Clay?",questions_only)
    
    def test_get_question_for_not_existing_category(self):
        catID = 2302
        res = self.client().get(f"/api/v1/categories/{catID}/questions")
        self.assertEqual(404,res.status_code)
    
    def test_quizz_endpoint(self):
        q = [5, 9, 12, 6]
        req = self.client().post("/api/v1/quizzes",json={
            'previous_questions': q,
            'quiz_category':  {
                "type": "click",
                "id": 0
            }
        })
        data =  json.loads(req.data)
        self.assertEqual(200,req.status_code)
        self.assertEqual(1,len(data))
        for q_id in q:
            self.assertNotEqual(q_id,data["question"]["id"])

    def test_quizz_endpoint_should_return_no_question_when_all_where_asked(self):
        r = range(1,60)
        q = list(r)
        req = self.client().post("/api/v1/quizzes",json={
            'previous_questions': q,
            'quiz_category':  {
                "type": "click",
                "id": 0
            }
        })
        data =  json.loads(req.data)
        self.assertFalse(data["question"])
            
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()