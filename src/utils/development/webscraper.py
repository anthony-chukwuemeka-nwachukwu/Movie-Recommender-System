from tkinter.messagebox import NO
from selenium import webdriver
from src.param import imdb_url, imdb_genres, imdb_years, get_year_index, get_genre_index
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from src.models import Review, User, Movie, Genre, db
from PIL import Image
import requests
from io import BytesIO



op = webdriver.ChromeOptions()
op.add_argument('headless')
try:
    driver.close()
except:
    pass
finally:
    driver = webdriver.Chrome(ChromeDriverManager().install(),options=op)

user_count=0

# These ids are necessary incase the program terminates and you wish to restart it, 
# just change these as needed based on the printed values
genre_id = get_genre_index('action')
year_id=get_year_index(2007)
col_id = 0


for ig in imdb_genres[genre_id:]:

    for imdb_year in imdb_years[::-1][year_id:]:

        driver.get(imdb_url( (ig, imdb_year)))
        col_title_len =  range(len( driver.find_elements(By.CLASS_NAME, 'col-title') ))

        for ct in col_title_len[col_id:]:
            print('========================Genre:{} - Year:{} - Movie:{}============================\n'.format(ig,imdb_year,ct))

            driver.implicitly_wait(2)
            driver.get(imdb_url( (ig, imdb_year)))
            col_title =  driver.find_elements(By.CLASS_NAME, 'col-title')

            # Title
            try:
                a_title = col_title[ct].find_element(By.TAG_NAME, 'a')
                title = a_title.text
            except:
                title = None

            # Img
            try:
                item_img =  driver.find_element(By.CLASS_NAME, 'lister-item-image')
                img_image = item_img.find_element(By.TAG_NAME, 'img')
                poster = img_image.get_attribute("src")
            except:
                continue

            
            # Url
            try:
                url = a_title.get_attribute("href")
            except:
                continue
            

            #id
            try:
                title_id = url.split('title')[1].split('/')[1]
            except:
                continue
            

            #Follow the link of movie i
            try:
                driver.get(url)
            except:
                continue
            

            #description
            try:
                description = driver.find_element(By.XPATH, './/section[@data-testid="Storyline"]')
                description = description.find_element(By.XPATH, './/div[@class="Storyline__StorylineWrapper-sc-1b58ttw-0 iywpty"]')
                description = description.find_element(By.XPATH, './/div[@data-testid="storyline-plot-summary"]')
                description = description.find_element(By.XPATH, './/div[@class="ipc-html-content ipc-html-content--base"]').text
            except:
                description =  None
            

            #release date
            try:
                release_date = driver.find_element(By.XPATH, './/section[@data-testid="Details"]')
                release_date = release_date.find_element(By.XPATH, './/div[@data-testid="title-details-section"]')
                release_date = release_date.find_element(By.XPATH, './/a[@class="ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link"]').text
            except:
                release_date = None
            

            #duration
            try:
                duration = driver.find_element(By.XPATH, './/section[@data-testid="TechSpecs"]')
                duration = duration.find_element(By.XPATH, './/div[@data-testid="title-techspecs-section"]')
                duration = duration.find_element(By.XPATH, './/li[@data-testid="title-techspec_runtime"]')
                duration = duration.find_element(By.CLASS_NAME, 'ipc-metadata-list-item__content-container').text
            except:
                duration = None
            

            #genre
            try:
                genre = driver.find_element(By.XPATH, './/section[@data-testid="Storyline"]')
                genre = genre.find_element(By.XPATH, './/div[@class="Storyline__StorylineWrapper-sc-1b58ttw-0 iywpty"]')
                genre = genre.find_element(By.XPATH, './/li[@data-testid="storyline-genres"]')
                genre = genre.find_elements(By.XPATH, './/li[@class="ipc-inline-list__item"]')
                genres = [i.text for i in genre]
            except:
                genres = []
            

            #director
            try:
                director = driver.find_element(By.XPATH, './/section[@data-testid="title-cast"]')
                director = director.find_element(By.XPATH, './/ul[@class="ipc-metadata-list ipc-metadata-list--dividers-all StyledComponents__CastMetaDataList-sc-y9ygcu-12 dXTKrS ipc-metadata-list--base"]')
                director = director.find_elements(By.TAG_NAME, 'li')[0]
                director = director.find_element(By.XPATH, './/a[@class="ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link"]').text
            except:
                director = None
        

            # Store in DB
            try:
                response = requests.get(poster)
                img = BytesIO(response.content).read()
            
                new_movie = Movie(id=title_id,title=title,url=url,poster=img,description=description,
                                release_date=release_date.split('(')[0].strip(),duration=duration.strip(),
                                director=director)
                db.session.add(new_movie)
                db.session.commit()
            except:
                continue
            

            for g in genres:
                try:
                    new_genre = Genre(name=g.lower(),movie_id=new_movie.id)
                    db.session.add(new_genre)
                    db.session.commit()
                except:
                    pass



            #Follow the link of movie i reviews
            
            # review url
            try:
                review_url = 'https://www.imdb.com/title/{}/reviews?sort=submissionDate&dir=desc'.format(title_id)
                driver.get(review_url)
                review_containers =  driver.find_elements(By.CLASS_NAME, 'review-container')
            except:
                continue

            for r in range(len(review_containers)):
                review_container = review_containers[r]

                # review star
                try:
                    ipl_ratings_bar = review_container.find_element(By.CLASS_NAME, 'ipl-ratings-bar')
                    rating_other_user_rating =  review_container.find_element(By.CLASS_NAME, 'rating-other-user-rating')
                    span_rating = rating_other_user_rating.find_elements(By.TAG_NAME, 'span')
                    review_star = [int(i.text.split('/')[::-1][0]) for i in span_rating]
                except:
                    review_star = [-1,100]
                    
                # review title
                try:
                    review_title = review_container.find_element(By.CLASS_NAME, 'title')
                except:
                    review_title = None
                    
                # review id 
                try:
                    review_href = review_title.get_attribute("href")
                    review_id = review_href.split('/')[-2]
                except:
                    continue
                
                # review
                try:
                    review_text = review_container.find_element(By.CLASS_NAME, 'text')
                except:
                    continue
                    
                # name of reviewer   
                try:
                    review_name = review_container.find_element(By.CLASS_NAME, 'display-name-link')
                except:
                    continue
                    
                # review date
                try:
                    review_date = review_container.find_element(By.CLASS_NAME, 'review-date')
                except:
                    review_date = None
                        

                    # Store in DB
                try:
                    new_user = User(username="imdb_"+review_name.text+"_"+str(user_count),password="imdb_password"+"_"+str(user_count))
                    db.session.add(new_user)

                    new_review = Review(id=review_id,url=review_url,star=(review_star[0]/review_star[1])*100,title=review_title.text,
                                    review=review_text.text,createdAt=review_date.text,updatedAt=review_date.text,
                                    username=new_user.username,movie_id=new_movie.id)
                    user_count += 1
                    db.session.add(new_review)
                    db.session.commit()
                except:
                    continue
        col_id=0
    year_id=0

