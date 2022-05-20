from src import db

def insert_like(movieid,user_name):
    query_like = """INSERT INTO movies_user_like(movie_id, username) VALUES('{}', '{}')""".format(movieid,user_name);
    query_dislike = """DELETE FROM movies_user_dislike WHERE movie_id='{}' AND username='{}';""".format(movieid,user_name)
    db.session.execute(query_like)
    db.session.execute(query_dislike)
    db.session.commit()

