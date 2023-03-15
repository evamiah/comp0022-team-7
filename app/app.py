from tkinter import E
from flask import Flask, render_template, redirect, request
from typing import List, Dict
import mysql.connector
import req1
import req5
import rating
import movie_details
import tags
import logging
import time
import init
from helpers import MovieViewer
from flask_paginate import Pagination, get_page_parameter

#docker compose setup from: https://www.devopsroles.com/deploy-flask-mysql-app-with-docker-compose/
app = Flask(__name__)

# for debugging
logging.basicConfig(level=logging.DEBUG)

config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'movie_db'
    }

MOVIES_PER_PAGE = 90

GENRES = [(1, 'Action'),
(2, 'Adventure'),
(3, 'Animation'),
(4, 'Children'),
(5, 'Comedy'),
(6, 'Crime'),
(7, 'Documentary'),
(8, 'Drama'),
(9, 'Fantasy'),
(10, 'Film-Noir'),
(11, 'Horror'),
(12, 'Musical'),
(13, 'Mystery'),
(14, 'Romance'),
(15, 'Sci-Fi'),
(16, 'Thriller'),
(17, 'War'),
(18, 'Western'),
(19, 'IMAX')]

FILTERS = ["Release Year", "Title",  "Genre", "Rating", "Popularity"]

def table_empty(table_name):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    query = 'SELECT COUNT(*) FROM ' + table_name
    cursor.execute(query)
    result = cursor.fetchone()
    if table_name == "people":
        #people table initialised with one value, "N/A"
        count = result[0] - 1
    else:
        count = result[0]
    cursor.close()
    connection.close()
    return count == 0 

def test_table(table_name) -> List[Dict]:
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    query = 'SELECT * FROM ' + table_name
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results

def clean_results(data):
    results = []
    for i in data:
        if type(i) is tuple:
            results.append(i[0])
        else:
            results.append(i)
    return results


@app.route('/q1')
def q1() -> str:
    startYear = None
    endYear = None
    rating = None
    title = None
    genre = None
    andOrOr = None
    sortBy = None
    mov_data = req1.getQuery(startYear, endYear, rating, title, genre, andOrOr, sortBy)
    return render_template('q1.html', data=mov_data)

@app.route('/q5')
def q5() -> str:
    movieId = "1"
    mov_data = req5.getQry(movieId)
    return render_template('q5.html', data=mov_data)

@app.route('/movie_genre')
def movie_genre() -> str:
    if table_empty('movie_genre'):
        init.load_movie_genre()
    mg_data = test_table('movie_genre')
    return render_template('test/movie_genre.html', data=mg_data)

@app.route('/movie_ratings')
def movie_ratings() -> str:
    if table_empty('movie_ratings'):
        init.load_movie_ratings()
    #mr_data = test_table('movie_ratings')
    mr_data = rating.analyse_ratings_genre('low', 1, 4)
    return render_template('test/movie_ratings.html', data=mr_data)

@app.route('/movie_links')
def movie_links() -> str:
    if table_empty('movie_links'):
        init.load_movie_links()
    ml_data = test_table('movie_links')
    return render_template('test/movie_links.html', data=ml_data)

@app.route('/movie_tags')
def movie_tags() -> str:
    if table_empty('movie_tags'):
        init.load_movie_tags()
    mt_data = test_table('movie_tags')
    return render_template('test/movie_tags.html', data=mt_data)

@app.route('/movies')
def movies() -> str:
    if table_empty('movies'):
        init.load_movies()
    movie_data = test_table('movies')
    return render_template('test/movies.html', data=movie_data)

@app.route('/people')
def people() -> str:
    if table_empty('people'):
        #init.load_empty_credit()
        init.load_people()
    movie_data = test_table('people')
    return render_template('test/people.html', data=movie_data)

@app.route('/cast')
def movie_cast() -> str:
    if table_empty('movie_cast'):
        init.load_cast()
    movie_data = test_table('movie_cast')
    return render_template('test/movie_cast.html', data=movie_data)

@app.route('/directing')
def movie_directing() -> str:
    if table_empty('movie_directing'):
        init.load_directors()
    movie_data = test_table('movie_directing')
    return render_template('test/movie_directing.html', data=movie_data)

@app.route('/q3')
def q3() -> str:
    test_data = []
    test_data.append(rating.analyse_ratings('low', 1)[0][0])
    test_data.append(rating.analyse_ratings('high', 1)[0][0])
    for i in range(1,20):
        test_data.append(rating.analyse_ratings_genre('low', 1, i)[0][0])
        test_data.append(rating.analyse_ratings_genre('high', 1, i)[0][0])
    return render_template('q3.html', data=test_data)

@app.route('/movies/<int:movie_id>')
def show_movie(movie_id):
    info = movie_details.select_movie(movie_id)
    cast = clean_results(movie_details.select_cast(movie_id))
    director = clean_results(movie_details.select_director(movie_id))
    invalid_request = False
    if not info:
        invalid_request = True
    else:
        info = info[0]
    movie = MovieViewer(info, cast, director, invalid_request)
    return render_template('movie_details.html', movie=movie.get_viewing_data())

@app.route('/q4')
def q4() -> str:
    #test_data = tags.analyse_tag_genre('Action')
    #test_data = tags.analyse_tag_rating_avg()
    #test_data = tags.analyse_tag_rating('high')
    #test_data = tags.analyse_tag_genre_totals()
    test_data = tags.analyse_tag_rating_totals()
    return render_template('q4.html', data=test_data)

@app.route('/search', methods = ['POST', 'GET'])
def search_title():
    if request.method == 'GET':
        return redirect('/')
    if request.method == 'POST':
        form_data = request.form
        results = movie_details.select_options(form_data['search_title'])
        search_results = []
        found = True
        if results:
            for info in results:
                m = MovieViewer(info)
                search_results.append(m.get_viewing_data())
        else:
            found = False
        return render_template('search.html', searched=form_data['search_title'], data=search_results, found=found)

@app.route('/filter', methods = ['POST', 'GET'])
def filter_movies():
    if request.method == 'GET':
        return redirect('/')
    if request.method == 'POST':
        form_data = request.form
        return render_template('filters.html', data = form_data)

@app.route('/')
def index() -> str:
    if table_empty('movies'):
        init.load_movies()
    movie_data = test_table('movies')
    search = False
    q = request.args.get('q')
    if q:
        search = True
    page = request.args.get(get_page_parameter(), type=int, default=1)
    offset = (page - 1) * MOVIES_PER_PAGE
    if (len(movie_data) - offset) > MOVIES_PER_PAGE:
        end = offset + MOVIES_PER_PAGE
    else:
        end = offset + (len(movie_data) % MOVIES_PER_PAGE)
    data = []
    page_data = movie_data[offset:end]
    for i in page_data:
        m = MovieViewer(i, [], [])
        data.append(m.get_viewing_data())
    pagination = Pagination(page=page, total=len(movie_data), per_page=MOVIES_PER_PAGE, search=search, record_name='movies')
    return render_template("home.html", data=data, genres=GENRES, filters=FILTERS, pagination=pagination)

#NOTE: temporarily as my browser autmotically add a trailing backslash to urls
@app.before_request
def clear_trailing():
    rp = request.path 
    if rp != '/' and rp.endswith('/'):
        return redirect(rp[:-1])

# loads all the tables when the first request is made, takes a while
# can be commented out if not all tables are needed
@app.before_first_request
def load_all():
    start_time = time.time()
    if table_empty('movies'):
        init.load_movies()
    if table_empty('people'):
        init.load_people()
    if table_empty('movie_genre'):
        init.load_movie_genre()
    if table_empty('movie_links'):
        init.load_movie_links()
    if table_empty('movie_ratings'):
        init.load_movie_ratings()
    if table_empty('movie_tags'):
        init.load_movie_tags()
    if table_empty('movie_cast'):
        init.load_cast()
    if table_empty('movie_directing'):
        init.load_directors()
    elapsed_time = time.time() - start_time
    logging.debug(f'Elapsed time: {elapsed_time} seconds')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port="5000")