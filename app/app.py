from flask import Flask, render_template
from typing import List, Dict
import mysql.connector
import json
import init

#docker compose setup from: https://www.devopsroles.com/deploy-flask-mysql-app-with-docker-compose/
app = Flask(__name__)

# flags used to check if the tables have been loaded
movies_loaded = False
movie_genre_loaded = False

def test_table(table_name) -> List[Dict]:
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'movie_db'
    }
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
    global movie_genre_loaded
    if not movie_genre_loaded:
        init.load_movie_genre()
        movie_genre_loaded = True
    mg_data = test_table('movie_genre')
    return render_template('movie_genre.html', data=mg_data)

@app.route('/movies')
def movies() -> str:
    global movies_loaded
    if not movies_loaded:
        init.load_movies()
        movies_loaded = True
    movie_data = test_table('movies')
    return render_template('movies.html', data=movie_data)


@app.route('/')
def index() -> str:
    movies = test_table('movies_table')
    return render_template('home.html', data=movies)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port="5000")