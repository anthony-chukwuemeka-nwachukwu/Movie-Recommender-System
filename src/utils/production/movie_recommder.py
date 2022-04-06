import os
import re
from turtle import title
from src import db
import numpy as np
import requests


class MovieRecommender:

    def __init__(self):

        genre_query = """SELECT genre,movie_id FROM genre"""
        self.genre = db.session.execute(genre_query).all()

        user_id_query = """SELECT DISTINCT username FROM movies_user_like"""
        user_ids = db.session.execute(user_id_query).all()

        user_query = """SELECT m.username,genre, COUNT(m.movie_id) AS movie_counts FROM movies_user_like m JOIN genre g ON m.movie_id = g.movie_id \
            GROUP BY (m.username,g.genre)"""
        self.user = db.session.execute(user_query).all()

        star_query = """SELECT movie_id,reviewer_username,star FROM reviews"""
        self.star = db.session.execute(star_query).all()

        
        movie_ids = set()
        movie_genries = set()
        self.user_ids = [self.__get_username(u[0]) for u in user_ids]

        for gi in self.genre: 
            movie_ids.add(gi[1])
            movie_genries.add(gi[0])

        self.movie_ids = list(movie_ids)
        self.movie_genries = list(movie_genries)


    def __get_username(self,string):
        if string.startswith("imdb"):
            string = "_".join(string.split("_")[:-1])
        return string

    def movies_by_genres(self):
        
        """Create a movie by genries matrix

        Returns:
            int: matrix of zeros and ones
        """

        movie_genre_matrix = np.zeros( (len(self.movie_ids), len(self.movie_genries)) )

        for gi in self.genre:
            i,j = self.movie_ids.index(gi[1]), self.movie_genries.index(gi[0])
            movie_genre_matrix[i,j] = 1
        
        return movie_genre_matrix

    def users_by_genres(self):

        user_genre_matrix = np.zeros( (len(self.user_ids), len(self.movie_genries)) )

        for ug in self.user:
            i,j = self.user_ids.index(self.__get_username(ug[0])), self.movie_genries.index(ug[1])
            user_genre_matrix[i,j] = ug[2]

        return user_genre_matrix


    def users_by_movies(self):

        user_movie_matrix = np.zeros( (len(self.user_ids), len(self.movie_ids)) )

        for s in self.star:
            if self.__get_username(s[1]) in self.user_ids:
                i = self.user_ids.index(self.__get_username(s[1]))
                j = self.movie_ids.index(s[0])
                user_movie_matrix[i,j] = s[2]                    

        return user_movie_matrix



#movieRecommender = MovieRecommender()
#movies = movieRecommender.get_movies_by_genries()
#print(movies)