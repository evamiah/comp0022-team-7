from typing import List, Dict
import mysql.connector

# for debugging
import logging
logging.basicConfig(level=logging.DEBUG)

config = {
        'user': 'team7',
        'password': 'G3LqY5UUTo0fK6x7nc7Q',
        'host': 'db',
        'port': '3306',
        'database': 'movie_db'
    }

def get_genre_id(genre) -> List[Dict]:
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    query = 'SELECT genre_id \
            FROM genres \
            WHERE genre = %s'
    cursor.execute(query, (genre,))
    results = cursor.fetchone()
    cursor.close()
    connection.close()
    return results

def analyse_ratings(value, movie_id) -> List[Dict]:
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    # returns the average rating of the movie by users who tend to rate movies lower (< 3.0)
    if value == 'low':
        query = 'SELECT AVG(rating) AS avg_low_rating \
            FROM movie_ratings \
            WHERE user_id IN ( \
                SELECT user_id \
                FROM movie_ratings \
                GROUP BY user_id \
                HAVING AVG(rating) < 3.0\
            ) \
            AND movie_id = %s'
    # returns the average rating of the movie by users who tend to rate movies higher (> 3.0)
    elif value == 'high':
        query = 'SELECT AVG(rating) AS avg_high_rating \
            FROM movie_ratings \
            WHERE user_id IN ( \
                SELECT user_id \
                FROM movie_ratings \
                GROUP BY user_id \
                HAVING AVG(rating) > 3.0\
            ) \
            AND movie_id = %s'
    cursor.execute(query, (movie_id,))
    results = cursor.fetchone()
    cursor.close()
    connection.close()
    return results

def analyse_ratings_genre(value, movie_id, genre_id) -> List[Dict]:
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    # returns the average rating of the movie by users who tend to rate movies of the given genre lower (< 3.0)
    if value == 'low':
        query = 'SELECT AVG(rating) AS avg_low_rating \
            FROM movie_ratings \
            WHERE user_id IN ( \
                SELECT user_id \
                FROM movie_ratings \
                WHERE movie_id IN ( \
                    SELECT movie_id \
                    FROM movie_genre \
                    WHERE genre_id = %s \
                ) \
                GROUP BY user_id \
                HAVING AVG(rating) < 3.0 \
            ) \
            AND movie_id = %s'
    # returns the average rating of the movie by users who tend to rate movies of the given genre higher (> 3.0)
    elif value == 'high':
        query = 'SELECT AVG(rating) AS avg_high_rating \
            FROM movie_ratings \
            WHERE user_id IN ( \
                SELECT user_id \
                FROM movie_ratings \
                WHERE movie_id IN ( \
                    SELECT movie_id \
                    FROM movie_genre \
                    WHERE genre_id = %s \
                ) \
                GROUP BY user_id \
                HAVING AVG(rating) > 3.0\
            ) \
            AND movie_id = %s'
    cursor.execute(query, (genre_id, movie_id,))
    results = cursor.fetchone()
    cursor.close()
    connection.close()
    return results