from typing import List, Dict
import mysql.connector

config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'movie_db'
    }

INVALID_ID = "Movie does not exist in the database."

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
        return INVALID_ID
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
        return INVALID_ID
    return results

def select_options(title):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    query = 'SELECT title, release_year, overview, poster_path \
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
    query = 'SELECT title, release_year, overview, poster_path \
                FROM movies \
                WHERE movie_id = %s'
    cursor.execute(query, (movie_id,))
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    if not results:
        return INVALID_ID
    return results



