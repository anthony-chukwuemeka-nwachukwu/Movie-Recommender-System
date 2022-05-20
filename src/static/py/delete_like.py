from src import db

def delete_like(movieid,user_name):
    query_dislike = """INSERT INTO movies_user_dislike(movie_id, username) VALUES('{}', '{}')""".format(movieid,user_name);
    query_like = """DELETE FROM movies_user_like WHERE movie_id='{}' AND username='{}';""".format(movieid,user_name)
    db.session.execute(query_like)
    db.session.execute(query_dislike)

    db.session.commit()