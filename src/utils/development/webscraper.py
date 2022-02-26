from io import BytesIO

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from src import db
from src.models.genre import Genre
from src.models.movie import Movie
from src.models.movies_user_like import MoviesUserLike
from src.models.review import Review
from src.models.user import User
from src.param import imdb_url, imdb_genres, imdb_years, get_year_index, get_genre_index

op = webdriver.ChromeOptions()
op.add_argument('headless')
try:
    driver.close()
except:
    pass
finally:
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=op)
wait_time = 50
# These ids are necessary in case the program terminates, and you wish to restart it,
# just change these as needed based on the printed values
genre_id = get_genre_index('family')
year_id = get_year_index(1988)
col_id = 0
user_count = 3060

for ig in imdb_genres[genre_id:]:

    for imdb_year in imdb_years[::-1][year_id:]:

        # driver.implicitly_wait(wait_time)
        driver.get(imdb_url((ig, imdb_year)))
        col_title_len = range(len(driver.find_elements(By.CLASS_NAME, 'col-title')))

        for ct in col_title_len[col_id:]:
            print(
                '======================== Genre:{} - Year:{} - Movie:{} - User Count:{} ============================\n'.format(
                    ig, imdb_year, ct, user_count))
            try:
                db.session.commit()
            except:
                pass

            # driver.implicitly_wait(wait_time)
            driver.get(imdb_url((ig, imdb_year)))
            col_title = driver.find_elements(By.CLASS_NAME, 'col-title')

            # Title
            try:
                a_title = col_title[ct].find_element(By.TAG_NAME, 'a')
                title = a_title.text
            except:
                title = ""

            # Img
            try:
                item_img = driver.find_element(By.CLASS_NAME, 'lister-item-image')
                img_image = item_img.find_element(By.TAG_NAME, 'img')
                poster = img_image.get_attribute("src")
            except:
                continue

            # Url
            try:
                url = a_title.get_attribute("href")
            except:
                continue

            # id
            try:
                title_id = url.split('title')[1].split('/')[1]
            except:
                continue

            # Follow the link of movie i

            try:
                # driver.implicitly_wait(wait_time)
                driver.get(url)
            except:
                continue

            # description
            try:
                description = driver.find_element(By.XPATH, './/section[@data-testid="Storyline"]')
                description = description.find_element(By.XPATH,
                                                       './/div[@class="Storyline__StorylineWrapper-sc-1b58ttw-0 iywpty"]')
                description = description.find_element(By.XPATH, './/div[@data-testid="storyline-plot-summary"]')
                description = description.find_element(By.XPATH,
                                                       './/div[@class="ipc-html-content ipc-html-content--base"]').text
            except:
                description = ""

            # release date
            try:
                release_date = driver.find_element(By.XPATH, './/section[@data-testid="Details"]')
                release_date = release_date.find_element(By.XPATH, './/div[@data-testid="title-details-section"]')
                release_date = release_date.find_element(By.XPATH,
                                                         './/a[@class="ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link"]').text
            except:
                release_date = ""

            # duration
            try:
                duration = driver.find_element(By.XPATH, './/section[@data-testid="TechSpecs"]')
                duration = duration.find_element(By.XPATH, './/div[@data-testid="title-techspecs-section"]')
                duration = duration.find_element(By.XPATH, './/li[@data-testid="title-techspec_runtime"]')
                duration = duration.find_element(By.CLASS_NAME, 'ipc-metadata-list-item__content-container').text
            except:
                duration = ""

            # genre
            try:
                genre = driver.find_element(By.XPATH, './/section[@data-testid="Storyline"]')
                genre = genre.find_element(By.XPATH, './/div[@class="Storyline__StorylineWrapper-sc-1b58ttw-0 iywpty"]')
                genre = genre.find_element(By.XPATH, './/li[@data-testid="storyline-genres"]')
                genre = genre.find_elements(By.XPATH, './/li[@class="ipc-inline-list__item"]')
                genres = [i.text for i in genre]
            except:
                genres = []

            # director
            try:
                director = driver.find_element(By.XPATH, './/section[@data-testid="title-cast"]')
                director = director.find_element(By.XPATH,
                                                 './/ul[@class="ipc-metadata-list ipc-metadata-list--dividers-all StyledComponents__CastMetaDataList-sc-y9ygcu-12 dXTKrS ipc-metadata-list--base"]')
                director = director.find_elements(By.TAG_NAME, 'li')[0]
                director = director.find_element(By.XPATH,
                                                 './/a[@class="ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link"]').text
            except:
                director = ""

            # Store in DB
            print("Movie")
            '''#query_id= """EXISTS(SELECT id FROM movies WHERE id='{}')""".format(title_id)
            query_id= """SELECT CASE WHEN EXISTS (SELECT id FROM movies WHERE id = '{}') 
            THEN CAST (1 AS BIT)
            ELSE CAST (0 AS BIT)
            END""".format(title_id)

            query_id = db.session.execute(query_id)'''

            try:
                print(title_id)
                response = requests.get(poster)
                img = BytesIO(response.content).read()

                new_movie = Movie(id=title_id, title=title, url=url, poster=img, description=description,
                                  release_date=release_date.split('(')[0], duration=duration,
                                  director=director)
                db.session.add(new_movie)
                db.session.commit()
            except:
                continue
            print("Genre")
            for g in genres:

                try:
                    new_movies_in_genre = Genre(g.lower(), title_id)
                    db.session.add(new_movies_in_genre)
                    db.session.commit()
                except:
                    pass

                # query_genre = """SELECT id FROM genres WHERE name='{}'""".format(g.lower())
                # genre_id = db.session.execute(query_genre).first()[0]

            # Follow the link of movie i reviews

            # review url

            try:
                review_url = 'https://www.imdb.com/title/{}/reviews?sort=submissionDate&dir=desc'.format(title_id)
                # driver.implicitly_wait(wait_time)
                driver.get(review_url)
                review_containers = driver.find_elements(By.CLASS_NAME, 'review-container')
            except:
                continue

            for r in range(len(review_containers)):
                review_container = review_containers[r]

                # review star
                try:
                    ipl_ratings_bar = review_container.find_element(By.CLASS_NAME, 'ipl-ratings-bar')
                    rating_other_user_rating = review_container.find_element(By.CLASS_NAME, 'rating-other-user-rating')
                    span_rating = rating_other_user_rating.find_elements(By.TAG_NAME, 'span')
                    review_star = [int(i.text.split('/')[::-1][0]) for i in span_rating]
                except:
                    review_star = [-1, 100]

                # review title
                try:
                    review_tit = review_container.find_element(By.CLASS_NAME, 'title')
                    review_title = review_tit.text
                except:
                    review_title = ""

                # review id 
                try:
                    review_href = review_tit.get_attribute("href")
                    review_id = review_href.split('/')[-2]
                except:
                    continue

                # review
                try:
                    review_text = review_container.find_element(By.CLASS_NAME, 'text').text
                except:
                    continue

                # name of reviewer   
                try:
                    review_name = review_container.find_element(By.CLASS_NAME, 'display-name-link').text
                except:
                    continue

                # review date
                try:
                    review_date = review_container.find_element(By.CLASS_NAME, 'review-date').text
                except:
                    review_date = ""

                # Store in DB
                print("User")
                try:
                    username = "imdb_" + review_name + "_" + str(user_count)
                    password = "imdb_password" + "_" + str(user_count)
                    star = (review_star[0] / review_star[1]) * 100

                    new_movie_user_like = MoviesUserLike(username, title_id)
                    new_review = Review(star=star, title=review_title,
                                        review=review_text, createdAt=review_date, updatedAt=review_date,
                                        reviewer_username=username, movie_id=title_id)
                    db.session.add(new_movie_user_like)
                    db.session.add(new_review)
                    db.session.commit()

                    if star >= 70.0:
                        new_user = User(username=username, password=password)
                        db.session.add(new_user)
                    db.session.commit()

                    user_count += 1

                except:
                    continue
        col_id = 0
    year_id = 0

if __name__ == '__main__':
    pass
