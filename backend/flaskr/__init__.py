from itertools import count
import os
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from random import randrange

from models import setup_db, Question, db, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    cors = CORS(app,resources={r"/api/*": {"origins": "*"}})

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """

    @app.route("/api/v1/categories", methods=['GET'])
    def list_categories():
        try:
            raw_data = [[cat[1],cat[0]] for cat in db.session.query(Category.id,Category.type).all()]
            categories = {}
            for cat in raw_data:
                categories[cat[1]]=cat[0]

            return jsonify({
                "success": True,
                "categories" : categories
            })

        except:
            return jsonify({
                "success": False,
                "message" : "An error occured while processing your request"
            }),422

        


    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route("/api/v1/questions", methods=['GET'])
    def get_questions_with_pagination():
        page = request.args.get('page',1,int)
        limit = 10
        offset = (page - 1) * limit

        raw_data = [[cat[1],cat[0]] for cat in db.session.query(Category.id,Category.type).all()]
        categories = {}
        for cat in raw_data:
            categories[cat[1]]=cat[0]
        
        if(page<1):
            return jsonify({
                "questions": [],
                "total_questions": Question.query.count(),
                "categories":categories,
                "currentCategory": "-"
            }),404

        questions = [question.format() for question in Question.query.offset(offset).limit(limit).all()]

        if len(questions) < 1 :
            return jsonify({
                "questions": [],
                "total_questions": Question.query.count(),
                "categories":categories,
                "currentCategory": "-"
            }),404

        
        return jsonify({
            "questions": questions,
            "total_questions": Question.query.count(),
            "categories" : categories,
            "currentCategory": "-"
        })

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    @app.route("/api/v1/questions/<int:question_id>", methods=['DELETE'])
    def delete_a_question(question_id):
        question = Question.query.get(question_id)
        try:
            db.session.delete(question)
            db.session.commit()
            return jsonify({
                "success" : True,
                "id" : question_id
            })
        except:
            db.session.rollback()
            return jsonify({
                "success" : False
            }),422


    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    @app.route("/api/v1/questions", methods=['POST'])
    def question_process():
        r = request.json
        if "searchTerm" not in r:
            try:
                data = request.json
                if data.get("difficulty") and data.get("question") and data.get("category") and data.get("difficulty"):
                    difficulty = int(data["difficulty"])
                    question = data["question"]
                    category = int(data["category"])
                    answer = data["answer"]

                    if (difficulty >= 0 and
                        difficulty <6 and
                        len(question)>2 and 
                        isinstance(question,str) and 
                        category >= 0 and 
                        isinstance(answer,str) and 
                        len(answer)>2):
                            question = Question(question=question,answer=answer,difficulty=difficulty,category=category)
                            db.session.add(question)
                            db.session.commit()
                            return jsonify({
                                "id" : question.id
                            })
                    else:
                        return jsonify({
                            "message" : "Your datas seems to not be well formated, can't process your request"
                        }),400
                else:
                    return jsonify({
                        "message" : "Some informations are missing, can't process your request"
                    }),400

            except:
                db.session.rollback()
                return jsonify({
                    "message" : "Your datas seems to not be well formated, can't process your request"
                }),400
        else:
            """
            @TODO:
            Create a POST endpoint to get questions based on a search term.
            It should return any questions for whom the search term
            is a substring of the question.

            TEST: Search by any phrase. The questions list will update to include
            only question that include that string within their question.
            Try using the word "title" to start.
            """
            raw_data = [[cat[1],cat[0]] for cat in db.session.query(Category.id,Category.type).all()]
            categories = {}
            for cat in raw_data:
                categories[cat[1]]=cat[0]
            

            questions = [question.format() for question in Question.query.filter(Question.question.ilike("%"+r["searchTerm"]+"%")).all()]

            if len(questions) < 1 :
                return jsonify({
                    "questions": [],
                    "total_questions": Question.query.count(),
                    "categories":categories,
                    "currentCategory": "-"
                }),200

            
            return jsonify({
                "questions": questions,
                "total_questions": Question.query.count(),
                "categories" : categories,
                "currentCategory": "-"
            })


    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    @app.route("/api/v1/categories/<int:category_id>/questions",methods=['GET'])
    def get_questions_per_category(category_id):
        categ = Category.query.get(category_id)
        if categ is None:
            return jsonify({
                "message":"Could not found the specified category"
            }),404

        questions = [question.format() for question in Question.query.join(Category,Question.category==Category.id).filter(Question.category==category_id).all()]
        return jsonify({
            "total_questions": Question.query.count(),
            "questions":questions,
            "currentCategory":categ.type
        })

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    @app.route("/api/v1/quizzes",methods=['POST'])
    def get_nex_quizz():
        try:
            req = request.json
            exclude = req["previous_questions"]
            categ = int(req["quiz_category"]["id"])
            if(categ==0): #get quizz from all categ
                all = [q.id for q in db.session.query(Question.id).all()]
            elif(categ>0 and categ<=6):
                all = [q.id for q in db.session.query(Question.id).filter(Question.category==categ).all()]
            else:
                raise Exception("Invalid Category")
            filtered = list(filter(lambda q_id : q_id not in exclude , all))
            if filtered:
                pos = randrange(0,len(filtered))
                choosen_id = filtered[pos]
                quizz = Question.query.get(choosen_id).format()
                return jsonify({
                    "question" : quizz
                })
            else:
                return jsonify({
                    "question" : []
                }),205
        except :
            return jsonify({
                "message" : "Your datas seems to not be well formated, can't process your request"
            }),400

    @app.errorhandler(404)
    def func_404(error):
        return jsonify({
            "message" : "Ressource could not be found on the server"
        }),404
    
    @app.errorhandler(422)
    def func_422(error):
        return jsonify({
            "message" : "The server was not able to process your request"
        }),422
    
    @app.errorhandler(405)
    def func_405(error):
        return jsonify({
            "message" : "HTTP Method not allowed for this route"
        }),405
    
    @app.errorhandler(500)
    def func_500(error):
        return jsonify({
            "message" : "An error occured on the server while processing your request"
        }),500
    
    
    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    return app

