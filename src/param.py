# This file contains all parameters used in the project


# imdb web scrapping
imdb_genres = ['action', 'adventure', 'animation', 'biography', 'comedy',
               'crime', 'documentary', 'drama', 'family', 'fantasy',
               'film-noir', 'history', 'horror', 'music', 'musical',
               'mystery', 'romance', 'sci-fi', 'short', 'sport',
               'superhero', 'thriller', 'war', 'western']
imdb_years = list(range(2003, 2023))
imdb_url = lambda \
        x: 'https://www.imdb.com/search/title/?genres={}&title_type=feature&year={}&view=simple&sort=user_rating,desc'.format(
    x[0], x[1])


def get_year_index(year):
    for i, y in enumerate(imdb_years[::-1]):
        if y == year:
            return i
    return


def get_genre_index(genre):
    for i, y in enumerate(imdb_genres):
        if y == genre:
            return i
    return


# Templates
app_title = 'More Flix'

# Sign in and out
signed_in = 'Sign In'
signed_out = 'Sign Out'

# Registration view
no_of_movie_per_genre = 15
min_required_no_of_movies_by_user = 2
no_imdb_genres = 18#len(imdb_genres)-1

# Movie view
no_of_similar_movies = 10

# Index, Movie recommendation

#model_filename = "/home/anthony/Documents/Strive/Movie-Recommender-System/src/utils/production/model.pickle"
model_filename = "src/utils/production/model.pickle"

if __name__ == '__main__':
    print(get_year_index(2009))
    print(get_genre_index('adventure'))
    print([i.lower() for i in []])
