from src import db

def insert_like(movieid,user_name):
    query = """INSERT INTO movies_user_like(movie_id, username) VALUES('{}', '{}')""".format(movieid,user_name);
    db.session.execute(query)
    db.session.commit()

