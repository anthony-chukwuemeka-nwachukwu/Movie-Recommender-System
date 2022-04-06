import copy
import re
import pandas as pd
from num2words import num2words
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import nltk
from src import db
import src.param as pm
from pandas.api.types import CategoricalDtype
from src.param import no_of_movie_per_genre, no_imdb_genres
from .search_feature_extraction import FeatureExtraction

nltk.download('stopwords')
nltk.download('punkt')


class Utils:

    def __init__(self):
        """
        Preprocesses document text queries
        """
        self.porter = PorterStemmer()
        self.stopwords = stopwords.words('english')

    def get_movie_descs(self):
        query = """SELECT id, name, description, url FROM movie"""
        movie = db.session.execute(query)
        return movie

    def liked_movie(self,t,u):
        query = """SELECT DISTINCT movie_id FROM movies_user_like WHERE movie_id='{}' AND username='{}'""".format(t,u)
        title = db.session.execute(query).all()
        #print(t,u,title)
        if title == []:
            return 'white'
        return 'orange'

    def similar_movies(self,t):
        query = """SELECT DISTINCT movie_id FROM movies_user_like WHERE movie_id='{}'""".format(t)
        title = db.session.execute(query).all()
        if title == []:
            return 'white'
        return 'orange'



    def process_single_document(self, doc):
        """
        preprocess single document
        :param doc: str
        :return: list(str)
        """
        alpn = re.sub(r'[^a-zA-Z0-9]', ' ', doc).lower()
        tokens = nltk.word_tokenize(alpn)

        filtered_words = [self.porter.stem(word) for word in tokens if word not in self.stopwords]
        words_without_nums = []
        for word in filtered_words:
            try:
                word = num2words(word).split('-')
                words_without_nums.extend(word)
            except:
                words_without_nums.append(word)
        return words_without_nums

    def process_documents(self, data):
        
        data['text'] = data.apply(lambda x: self.process_single_document(str(x['title'])+' '+str(x['description'])), axis=1)

        return data

    def process_query(self, text):
        tokens = self.process_single_document(text)
        return tokens

    def ranked_ids(self, query, data):
        df = copy.deepcopy(data)
        
        processed_resumes = self.process_documents(df)

        featureExtraction = FeatureExtraction()
        processed_query = self.process_query(query)
        fe = featureExtraction.generate_features(processed_resumes, processed_query)

        #return fe.id.values, fe.mean_tfidf.values, fe.bm25.values, self.normalize(fe.drop(['id', 'name', 'description'], axis=1).values)

        x = [x for _,x in sorted(zip(list(fe.bm25.values) ,list(fe.id.values)), reverse=True)]
        y = [y for y,_ in sorted(zip(list(fe.bm25.values) ,list(fe.id.values)), reverse=True)]
        

        return x,y

    def search_movies(self,query):
        # get movie titles in genres
        genres = """SELECT DISTINCT genre FROM genre"""
        genres = [g[0] for g in db.session.execute(genres).all()][:pm.no_imdb_genres]

        movie_all = {}
        genres_query = lambda g: """SELECT DISTINCT movie_id FROM genre WHERE genre='{}'""".format(g)
        movie_query = lambda m: """SELECT id, title, poster_address, url, duration, director, description FROM movies WHERE id='{}'""".format(m)

        unique_titles = []
        genre_scores = []
        for genre in genres:
            movies = [db.session.execute(movie_query(g[0])).all() for g in
                    db.session.execute(genres_query(genre)).all()]
            new_movies = []
            items = []
            for movie in movies:
                items.append(movie[0][0])
                if movie[0][0] not in unique_titles:
                    unique_titles.append(movie[0][0])
                    new_movie = []
                    for i, m in enumerate(movie[0]):

                        if i == 2:
                            #new_movie.append(base64.b64encode(m).decode("utf-8"))
                            new_movie.append(m)
                        else:
                            new_movie.append(m)
                    new_movies.append(new_movie)
                
            df = pd.DataFrame(new_movies, columns =['id', 'title', 'poster', 'url', 'duration', 'director', 'description'])

            #ranking       
            rank_ids,rank_scores=self.ranked_ids(query, df)
            genre_scores.append(sum(rank_scores))
            
            id_order = CategoricalDtype(rank_ids, ordered=True)
            df['id'] = df['id'].astype(id_order)
            df = df.sort_values('id')

            #movie_genre.append(df.head(pm.no_of_movie_per_genre).values)

            tdf = list(df.itertuples(index=False, name=None))

            movie_all[genre.capitalize()] = tdf[:pm.no_of_movie_per_genre]

        indices_genre_scores = [i[0] for i in sorted(enumerate(genre_scores), reverse=True, key=lambda x:x[1])]
        sorted_genres = [list(movie_all.keys())[index] for index in indices_genre_scores]
    
        return movie_all, sorted_genres

    def get_movies(self):
        # get movie titles in genres
        genres = """SELECT DISTINCT genre FROM genre"""
        genres = [g[0] for g in db.session.execute(genres).all()][:no_imdb_genres]

        movie_all = {}
        genres_query = lambda g: """SELECT DISTINCT movie_id FROM genre WHERE genre='{}'""".format(g)
        movie_query = lambda m: """SELECT DISTINCT id, title, poster_address, url, duration, director, description FROM movies WHERE id='{}'""".format(m)

        unique_titles = []
        for genre in genres:
            movies = [db.session.execute(movie_query(mid[0])).all() for mid in db.session.execute(genres_query(genre)).all()]
            
            new_movies = []
            for movie in movies:
                if movie and movie[0][0] not in unique_titles:
                    unique_titles.append(movie[0][0])
                    new_movie = []
                    for i, m in enumerate(movie[0]):

                        if i == 2:
                            #new_movie.append(base64.b64encode(m).decode("utf-8"))
                            new_movie.append(m)
                        else:
                            new_movie.append(m)
                    new_movies.append(new_movie)
            
            movie_all[genre.capitalize()] = new_movies[:no_of_movie_per_genre]

        return movie_all, list(movie_all.keys())

    
    def rank_movies(self,query, movie_id):

        movie_all = {}
        movie_query = """SELECT DISTINCT m.id, m.title, m.poster_address, m.url, m.duration, m.director, m.description, g.genre FROM movies m JOIN genre g ON g.movie_id = m.id"""

        unique_titles = []
        movies = db.session.execute(movie_query).all()
        new_movies = []
        for movie in movies:
            
            if movie[0] not in unique_titles and movie[0] != movie_id:
                unique_titles.append(movie[0])
                new_movie = []
                for i, m in enumerate(movie):

                    if i == 2:
                        #new_movie.append(base64.b64encode(m).decode("utf-8"))
                        new_movie.append(m)
                    else:
                        new_movie.append(m)
                new_movies.append(new_movie)
                
        df = pd.DataFrame(new_movies, columns =['id', 'title', 'poster_address', 'url', 'duration', 'director', 'description', 'genre'])

        #ranking       
        rank_ids,_=self.ranked_ids(query, df)
        
        id_order = CategoricalDtype(rank_ids, ordered=True)
        df['id'] = df['id'].astype(id_order)
        df = df.sort_values('id')

        tdf = list(df.itertuples(index=False, name=None))[:pm.no_of_similar_movies]
    
        return tdf




if __name__ == '__main__':
    utils = Utils()
    df=utils.get_movie_descs()
    p=utils.ranked_ids('love', df)
    print(p[:2])
