# Movie-Recommender-System
An AI empowered movie recommender system with powerful search engine.

## Description
This is a web-based app that provides personalized movie recommendation to the user. 
The user is first required to create account, during which process he is to like some 
movies which would be added to his liked list and used as initial movie recommendation 
for him.  

Upon login, a personalised movie recommendations based on the users likes and other 
users with similar likes as the user is made to the user. The algorithm used is the 
collaborative filtering and implemented with a ridge regression model.

The user is also able to search for movies available in the database using the search 
field. The returned movies are ranked based on the bm25 scores. The genres are scored 
and presented based on the total scores of the movies contained in them.

Both the collaborative filtering and bm25 were implemented from scratch.

## Usage
To use this repo,
- first run the requirement file to install the dependencies  
`pip3 install --no-cache-dir -r ./requirements.txt`  
- then proceed to run the wsgi file  
`python wsgi.py`


## Technologies Used
1. Frontend
- HTML5
- CSS3
- Bootstrap
- Javascript
2. Backend
- Flask
- flask-sqlalchemy
- flask_marshmallow
- marshmallow-sqlalchemy
- wtforms
- flask_session
psycopg2
3. Webscrapping
- chrome
- selenium
4. AI
- sklearn
- nltk
- numpy
- pandas
- pytorch

