from src import db

def delete_like(movieid):

    query = """DELETE FROM movies_user_like WHERE movie_id='{}';""".format(movieid)
    db.session.execute(query)
    db.session.commit()