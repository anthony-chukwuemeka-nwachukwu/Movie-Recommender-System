from flask import Blueprint, jsonify, render_template
from src import db
from src.models.user import User
from src.models.review import review_schemas
from src.models.movie import movie_schemas

profile = Blueprint('profile', __name__)

@profile.route('/profile/<user_id>', methods=['GET'])
def user_profile(user_id):
    username = db.session.query(User).filter(User.username == user_id).first()
    user = User.query.filter_by(username=user_id).first_or_404()
    print("===============================")
    liked_movies = movie_schemas.dump(username.liked_movies)
    reviews = review_schemas.dump(username.reviews)
    print(reviews)

    return jsonify(user.serialize)#user_schema.dump(username)#
    
    """try:
        username = db.session.query(User).filter(User.username == user_id).first()
        print("===============================")
        username.liked_movies = movie_schemas.dump(username.liked_movies)
        username.reviews = review_schemas.dump(username.reviews)

        return user_schema.dump(username)#render_template('profile.html')
    except:
        return {'Error':'invalid user'}"""