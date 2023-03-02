from flask import Flask, render_template
from typing import List, Dict
import mysql.connector
import json
import init
import rating
import logging
import time
import subprocess

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

def table_empty(table_name):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    query = 'SELECT COUNT(*) FROM ' + table_name
    cursor.execute(query)
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result[0] == 0 

def test_table(table_name) -> List[Dict]:
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    query = 'SELECT * FROM ' + table_name
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results

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

@app.route('/q3')
def q3() -> str:
    test_data = []
    test_data.append(rating.analyse_ratings('low', 1)[0][0])
    test_data.append(rating.analyse_ratings('high', 1)[0][0])
    for i in range(1,20):
        test_data.append(rating.analyse_ratings_genre('low', 1, i)[0][0])
        test_data.append(rating.analyse_ratings_genre('high', 1, i)[0][0])
    return render_template('q3.html', data=test_data)

@app.route('/')
def index() -> str:
    movies = test_table('movies_table')
    return render_template('home.html', data=movies)

# loads all the tables when the first request is made, takes a while
# can be commented out if not all tables are needed
@app.before_first_request
def load_all():
    start_time = time.time()
    if table_empty('movies'):
        init.load_movies()
    if table_empty('movie_genre'):
        init.load_movie_genre()
    if table_empty('movie_links'):
        init.load_movie_links()
    if table_empty('movie_ratings'):
        init.load_movie_ratings()
    if table_empty('movie_tags'):
        init.load_movie_tags()
    elapsed_time = time.time() - start_time
    logging.debug(f'Elapsed time: {elapsed_time} seconds')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port="5000")