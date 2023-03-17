from typing import List, Dict
import mysql.connector
from extension_scripts import get_rt_ratings

config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'movie_db'
    }

INVALID_ID = "Movie does not exist in the database."

def get_invalid_id():
    return INVALID_ID

def select_cast(movie_id):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    query = 'SELECT full_name \
                FROM people \
                INNER JOIN movie_cast  \
                ON people.person_id = movie_cast.actor_id \
                INNER JOIN movies \
                ON movie_cast.movie_id = movies.movie_id \
                WHERE movies.movie_id = %s'
    cursor.execute(query, (movie_id,))
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    if not results:
        return []
    return results


def select_director(movie_id):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    query = 'SELECT full_name \
                FROM people \
                INNER JOIN movie_directing  \
                ON people.person_id = movie_directing.director_id \
                INNER JOIN movies \
                ON movie_directing.movie_id = movies.movie_id \
                WHERE movies.movie_id = %s'
    cursor.execute(query, (movie_id,))
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    if not results:
        return []
    return results

def select_options(title):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    query = 'SELECT movie_id, title, release_year, overview, poster_path \
                FROM movies \
                WHERE title LIKE %s'
    cursor.execute(query, ('%' + title + '%',))
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results


def select_movie(movie_id):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    query = 'SELECT movie_id, title, release_year, overview, poster_path \
                FROM movies \
                WHERE movie_id = %s'
    cursor.execute(query, (movie_id,))
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    if not results:
        return []
    return results

def select_rt_rating(movie_id):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    query = 'SELECT tomatometer, audience_score \
                FROM rt_ratings \
                WHERE movie_id = %s'
    cursor.execute(query, (movie_id,))
    results = cursor.fetchone()
    cursor.close()
    connection.close()
    if not results:
        return []
    return results

def get_tmdb_id(movie_id):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    query = 'SELECT tmdb_id\
                FROM movie_links \
                WHERE movie_id = %s'
    cursor.execute(query, (movie_id,))
    results = cursor.fetchone()
    cursor.close()
    connection.close()
    return results

def insert_rt_rating(movie_id, title, year):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    tmdb_id = get_tmdb_id(movie_id)[0]
    ratings = get_rt_ratings(movie_id, tmdb_id, title, year)
    if ratings:
        tomatometer = int(ratings[0])
        audience_score = int(ratings[1])
    else:
        tomatometer = -1
        audience_score = -1
    cursor.execute('INSERT INTO rt_ratings (movie_id, tomatometer, audience_score) VALUES (%s, %s, %s);', (movie_id, tomatometer, audience_score))
    connection.commit()
    cursor.close()
    connection.close()


