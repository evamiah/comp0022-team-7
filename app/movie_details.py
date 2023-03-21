from typing import List, Dict
import mysql.connector
from extension_scripts import get_rt_ratings, get_basic_info

config = {
        'user': 'team7',
        'password': 'G3LqY5UUTo0fK6x7nc7Q',
        'host': 'db',
        'port': '3306',
        'database': 'movie_db'
    }

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

# returns movies with title similar to searched title
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

def update_movie_year(movie_id, year):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    query = 'UPDATE movies \
                SET release_year = %s \
                WHERE movie_id = %s'
    cursor.execute(query, (year, movie_id))
    connection.commit()
    cursor.close()
    connection.close()

def use_tmdb_year(movie_id):
    tmdb_id = get_tmdb_id(movie_id)[0]
    year = get_basic_info(tmdb_id, movie_id)[2]
    if year:
        update_movie_year(movie_id, year)
        return year
    return 0

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

# select a movie's average user rating rounded to 1dp
def aggregate_rating(movie_id):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    query = 'SELECT ROUND(AVG(mr.rating),1) FROM movie_ratings AS mr WHERE mr.movie_id = %s GROUP BY mr.movie_id'
    cursor.execute(query, (movie_id,))
    results = cursor.fetchone()
    cursor.close()
    connection.close()
    return results

def get_genres(movie_id):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    query = 'SELECT g.genre_id, g.genre \
                FROM genres AS g \
                INNER JOIN movie_genre AS mg \
                ON mg.genre_id = g.genre_id \
                INNER JOIN movies \
                ON mg.movie_id = movies.movie_id \
                WHERE movies.movie_id = %s'
    cursor.execute(query, (movie_id,))
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    if not results:
        return []
    return results

# get genres listed in a single string
def list_genres(movie_id):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    query = 'SELECT GROUP_CONCAT(DISTINCT g.genre ORDER BY g.genre ASC) AS genre_list\
        FROM movie_genre AS mg \
        INNER JOIN \
        genres AS g \
        ON mg.genre_id = g.genre_id \
        WHERE mg.movie_id = %s GROUP BY mg.movie_id'
    cursor.execute(query, (movie_id,))
    results = cursor.fetchone()
    cursor.close()
    connection.close()
    return results

# popularity measured by the number of votes received
def get_popularity(movie_id):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    query = 'SELECT COUNT(mr.user_id) FROM movie_ratings AS mr WHERE mr.movie_id = %s GROUP BY mr.movie_id'
    cursor.execute(query, (movie_id,))
    results = cursor.fetchone()
    cursor.close()
    connection.close()
    return results