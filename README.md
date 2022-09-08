
# Trivia API

Welcome!

Trivia is a wonderful quiz game where a user is invited to 
answer questions and get scored after!

Questions are of any or choosen category.

[Screencast](https://user-images.githubusercontent.com/35831811/188739899-bb3fa937-8c86-4125-b228-70903fc33cf7.webm)

# Getting started

The app implement both the api for all the functionalities 
you need for a trivia game and additionaly a frontend that
help you play the game on a graphical User interface.

- For runing the backend (APi) please visit this [link](https://github.com/ElvisAns/Trivia-API/tree/main/frontend#readme)
- For runing the frontend and actually test the app visit this [link](https://github.com/ElvisAns/Trivia-API/tree/main/backend#readme) 


## API Reference

#### Get all quiz categories

```http
GET /api/v1/categories
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| None | - | Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category|

***Sample Response body***

```json
    {
        "categories": {
            "1": "Science",
            "2": "Art",
            "3": "Geography",
            "4": "History",
            "5": "Entertainment",
            "6": "Sports"
        }
    }
```
#### Get paginated questions

```http
GET /api/v1/questions?page=${integer}
```

| Parameter | Type     | Description                |Returns|
| :-------- | :------- | :------------------------- |:-------|
| **Required:**  `page` | `integer` | Fetches a paginated set of questions, a total number of questions, all categories and current category string| An object with 10 paginated questions, total questions, object including all categories, and current category string|

***Sample Response body***

```json
    {
        "questions": [
            {
            "id": 1,
            "question": "This is a question",
            "answer": "This is an answer",
            "difficulty": 5,
            "category": 2
            }
        ],
        "totalQuestions": 100,
        "categories": {
            "1": "Science",
            "2": "Art",
            "3": "Geography",
            "4": "History",
            "5": "Entertainment",
            "6": "Sports"
        },
        "currentCategory": "History"
    }
```

#### Get all question within a category

```http
GET /api/v1/categories/${id}/questions
```

| Parameter | Type     | Description                |Returns|
| :-------- | :------- | :------------------------- |:-------|
| **Required:**  `id` | `integer` | Fetches questions for a cateogry specified by id request argument | An object with questions for the specified category, total questions, and current category string|

***Sample Response body***

```json
    {
        "questions": [
            {
            "id": 1,
            "question": "This is a question",
            "answer": "This is an answer",
            "difficulty": 5,
            "category": 4
            }
        ],
        "totalQuestions": 100,
        "currentCategory": "History"
    }
```

#### Delete a question

```http
DELETE /api/v1/questions/${id}
```

| Parameter | Type     | Description                |Returns|
| :-------- | :------- | :------------------------- |:-------|
| **Required:** `id` | `integer` | Deletes a specified question using the id of the question| The ID of the deleted question |

***Sample Response body***

```json

    {
        "success" : true,
        "id" : 10
    }
```

#### Get a random question to play the quiz

```http
POST /api/v1/quizzes
```
***Sample Request body***

```json
    {
        "previous_questions": [1, 4, 20, 15],
        "quiz_category": "History"
    }

```

| Param | Type     | Description                |Returns|
| :-------- | ------- | :------------------------- |:-------|
| **Required:** `The request body` | `json` |Sends a post request in order to get the next question| A single new question object|

***Sample Response body***

```json
    {
        "question": {
            "id": 1,
            "question": "This is a question",
            "answer": "This is an answer",
            "difficulty": 5,
            "category": 4
        }
    }

```
#### Add new question

```http
POST /api/v1/questions
```

| Parameter | Type     | Description                |Returns|
| :-------- | :------- | :------------------------- |:-------|
| **Required:**  `Request Body` | `json` | Sends a post request in order to add a new question | The ID of the new question |

***Sample Request body***

```json
    {
        "question": "Heres a new question string",
        "answer": "Heres a new answer string",
        "difficulty": 1,
        "category": 3
    }
```
***Sample Response body***

```json
{
  "id": 38
}

```

#### Get all questions matching a search term

```http
POST /api/v1/questions
```

| Parameter | Type     | Description                |Returns|
| :-------- | :------- | :------------------------- |:-------|
| **Required:**  `Request Body` | `json` | Sends a post request in order to search for a specific question by search term | Any array of questions, a number of totalQuestions that met the search term and the current category string|

***Sample Request body***

```json
{
  "searchTerm": "this is the term the user is looking for"
}
```
***Sample Response body***

```json
{
  "questions": [
    {
      "id": 1,
      "question": "This is a question",
      "answer": "This is an answer",
      "difficulty": 5,
      "category": 5
    }
  ],
  "totalQuestions": 100,
  "currentCategory": "Entertainment"
}

```
## Acknowledgements

- [Udacity](udacity.com) And all the lecturers over there


## Screenshots

![image](https://user-images.githubusercontent.com/35831811/188736562-ac8286a3-420f-4677-8531-282e9a0a0d56.png)


## 🛠 Built With
React, Javascript, Python, Flask, SQLAlchemy ORM, PostgreSQL...


## Authors

- [@ElvisAnsima](http://github.com/ElvisAns)


## 🚀 About Me
I'm a generalist web developer & entrepreneur, driven by curiosity, positivity, and a can-do attitude;i like to code web application projects with various stack.

