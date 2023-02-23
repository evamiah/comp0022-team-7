from flask import Flask, render_template
from typing import List, Dict
import mysql.connector
import json
import init

#docker compose setup from: https://www.devopsroles.com/deploy-flask-mysql-app-with-docker-compose/
app = Flask(__name__)

movies_loaded = False

def test_table() -> List[Dict]:
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'movie_db'
    }
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM movies_table')
    results = cursor.fetchall()
    # results = [{movie_id: title} for (movie_id, title) in cursor]
    cursor.close()
    connection.close()

    return results

def movies_table() -> List[Dict]:
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'movie_db'
    }
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM movies')
    results = cursor.fetchall()
    cursor.close()
    connection.close()

    return results

@app.route('/movies')
def movies() -> str:
    global movies_loaded
    if not movies_loaded:
        init.load_movies()
        movies_loaded = True
    #return json.dumps({'test_table': test_table()})
    movie_data = movies_table()
    return render_template('movies.html', data=movie_data)


@app.route('/')
def index() -> str:
    #return json.dumps({'test_table': test_table()})
    movies = test_table()
    return render_template('home.html', data=movies)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port="5000")