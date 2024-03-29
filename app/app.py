from flask import Flask, render_template, redirect, request
from typing import List, Dict
import mysql.connector
import req1_filter
import movie_details
import tags
import logging
import time
import init
import json
from helpers import MovieViewer, StatsViewer, get_genre
from flask_paginate import Pagination, get_page_parameter


app = Flask(__name__)

# for debugging
logging.basicConfig(level=logging.DEBUG)

config = {
        'user': 'team7',
        'password': 'G3LqY5UUTo0fK6x7nc7Q',
        'host': 'db',
        'port': '3306',
        'database': 'movie_db'
    }

MOVIES_PER_PAGE = 90
FILTERS = ["Release Year", "Title",  "Genre", "Rating", "Popularity"]


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

# selects all records from a table
def test_table(table_name) -> List[Dict]:
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    query = 'SELECT * FROM ' + table_name
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results

# get start/end limits of data to show depending on page number 
def get_page_limits(page, movie_data):
    offset = (page - 1) * MOVIES_PER_PAGE
    if (len(movie_data) - offset) > MOVIES_PER_PAGE:
        end = offset + MOVIES_PER_PAGE
    else:
        end = offset + (len(movie_data) % MOVIES_PER_PAGE)
    return offset, end

# makes an array from tuples returned from queries
def clean_results(data):
    results = []
    for i in data:
        if type(i) is tuple:
            results.append(i[0])
        else:
            results.append(i)
    return results

# returns rotten tomatoes ratings after checking they exist in the db yet
def check_rt(movie_id, info):
    rt_ratings = movie_details.select_rt_rating(movie_id)
    if not rt_ratings and (info):
        movie_details.insert_rt_rating(movie_id, info[1], info[2])
        rt_ratings = movie_details.select_rt_rating(movie_id)
    return rt_ratings

@app.route('/movies/<int:movie_id>/stats/<value_1>/<int:genre_id>/<value_2>')
def movie_stats(movie_id, value_1, genre_id, value_2):
    info = movie_details.select_movie(movie_id)
    invalid_request = False
    if not info:
        invalid_request = True
    else:
        info = info[0]
        genres = movie_details.get_genres(movie_id)
        stats = StatsViewer(movie_id, genres)
        movie = MovieViewer(info, invalid_movie=invalid_request)
        genre_name = get_genre(genre_id)[0][0]
        
    return render_template('movie_stats.html', stats_data=stats.get_movie_stats(), movie=movie.get_viewing_data(), genre_name=genre_name, value_1=value_1, value_2=value_2, movie_id=movie_id, genre_id=genre_id, genres=genres)

@app.route('/movies/<int:movie_id>')
def show_movie(movie_id):
    info = movie_details.select_movie(movie_id)
    cast = clean_results(movie_details.select_cast(movie_id))
    director = clean_results(movie_details.select_director(movie_id))
    invalid_request = False
    if not info:
        invalid_request = True
        rt_ratings = []
    else:
        info = info[0]
        rt_ratings = check_rt(movie_id, info)
        genre_id = movie_details.get_genres(movie_id)[0][0]
    movie = MovieViewer(info, rt_ratings, cast, director, full_details=True, invalid_movie=invalid_request)
    return render_template('movie_details.html', movie=movie.get_viewing_data(), genre_id=genre_id, movie_id=movie_id)

# returns search title results
@app.route('/search', methods = ['POST', 'GET'])
def search_title():
    if request.method == 'GET':
        return redirect('/')
    if request.method == 'POST':
        form_data = request.form
        if form_data.get('match_whole'):
            results = movie_details.select_options(form_data['search_title'], True)
        else:
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

# returns filtered movie results
@app.route('/filter', methods = ['POST', 'GET'])
def filter_movies():
    if request.method == 'GET':
        return redirect('/')
    if request.method == 'POST':
        form_data = request.form
        genre_list = []
        for genre in GENRES:
            val = request.form.get(genre[1])
            if val:
                genre_list.append(genre[1])
        results = req1_filter.get_query(form_data['start_year'], form_data['end_year'], form_data['sort_by'], form_data['order'], genre_list, form_data['genre_and_or'], form_data['rating'])
        
        filter_results = []
        found = True
        if results:
            for info in results:
                m = MovieViewer(info)
                filter_results.append(m.get_viewing_data())
        else:
            found = False

        # pass value being sorted
        sorting_data = [form_data['sort_by']]
        if (form_data['sort_by'] == "Release Year"):
            sorting_data.append('year')
        elif (form_data['sort_by'] == "Title"):
            sorting_data.append('title')
        elif (form_data['sort_by'] == "Genre"):
            sorting_data.append('genre')
        elif (form_data['sort_by'] == "Rating"):
            sorting_data.append('user_rating')
        else:
            sorting_data.append('popularity')
        
        return render_template('filter.html', data=filter_results, sorting_data=sorting_data, found=found)
    
@app.route('/tag_analysis/<int:genre_id>')
def chart(genre_id) -> str:
    rating_totals = tags.analyse_tag_rating_totals()
    genre_totals = tags.analyse_tag_genre_totals()
    low_rating = tags.analyse_tag_rating_avg('low')
    high_rating = tags.analyse_tag_rating_avg('high')
    genre = tags.analyse_tag_genre(genre_id)
    genre_rating = tags.analyse_tag_rating_genre(genre_id)
    current_genre = get_genre(genre_id)
    return render_template('tag_analysis.html', rating_totals=rating_totals, genre_totals=genre_totals, low_rating=json.dumps(low_rating),high_rating=json.dumps(high_rating), genre=json.dumps(genre), genre_rating=json.dumps(genre_rating), current_genre=json.dumps(current_genre))


@app.route('/')
def index() -> str:
    if table_empty('movies'):
        init.load_movies()
    movie_data = test_table('movies')
    page = request.args.get(get_page_parameter(), type=int, default=1)
    offset, end = get_page_limits(page, movie_data)
    data = []
    page_data = movie_data[offset:end]
    for i in page_data:
        m = MovieViewer(i)
        data.append(m.get_viewing_data())
    pagination = Pagination(page=page, total=len(movie_data), per_page=MOVIES_PER_PAGE, record_name='movies')
    return render_template("home.html", data=data, genres=GENRES, filters=FILTERS, pagination=pagination)

#NOTE: occasionally browsers autmotically add a trailing backslash to urls
@app.before_request
def clear_url():
    url = request.path 
    if url != '/' and url.endswith('/'):
        return redirect(url[:-1])

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

