# This file contains all parameters used in the project


# imdb web scrapping
imdb_genres = ['action','adventure','animation','biography','comedy',
                'crime','documentary','drama','family','fantasy',
                'film-noir','history','horror','music','musical',
                'mystery','romance','sci-fi','short','sport',
                'superhero','thriller','war','western']
imdb_years = list(range(1900,2023))
imdb_url = lambda x:'https://www.imdb.com/search/title/?genres={}&title_type=feature&year={}&view=simple&sort=user_rating,desc'.format(x[0],x[1])

def get_year_index(year):
    for i,y in enumerate(imdb_years[::-1]):
        if y == year:
            return i
    return

def get_genre_index(genre):
    for i,y in enumerate(imdb_genres):
        if y == genre:
            return i
    return

if __name__=="__main__":
    print(get_year_index(2009))
    print(get_genre_index('adventure'))