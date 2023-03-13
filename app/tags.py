from typing import List, Dict
import mysql.connector

# for debugging
import logging
logging.basicConfig(level=logging.DEBUG)

config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'movie_db'
    }

# returns the tags that have been applied to movies in a cetrain genre, ordered by the amount of times they have been applied
def analyse_tag_genre(genre) -> List[Dict]:
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    query = 'SELECT tag, COUNT(*) as tag_count \
            FROM movie_tags \
            JOIN movie_genre ON movie_tags.movie_id = movie_genre.movie_id \
            JOIN genres ON movie_genre.genre_id = genres.genre_id \
            WHERE genre = %s \
            GROUP BY tag \
            ORDER BY tag_count DESC'
    cursor.execute(query, (genre,))
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results

# returns the tags listed in order of the average ratings of all the movies the tags have been applied to
def analyse_tag_rating_avg() -> List[Dict]:
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    query = 'SELECT tag, AVG(rating_avg) AS tag_rating\
            FROM \
                (SELECT \
                    movie_id, \
                    AVG(rating) AS rating_avg \
                    FROM movie_ratings \
                    GROUP BY movie_id) AS avg_ratings \
            JOIN movie_tags ON avg_ratings.movie_id = movie_tags.movie_id \
            GROUP BY tag\
            ORDER BY tag_rating DESC'
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results

# returns the tags applied to movies with an average rating < 3.0 (if value ='low') or > 3.0 (if value ='high') ordered by
# how many times they have been applied 
def analyse_tag_rating(value) -> List[Dict]:
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    if value == 'low':
        query = 'SELECT tag, COUNT(*) AS tag_count \
                FROM \
                (SELECT \
                    movie_id, \
                    AVG(rating) AS rating_avg \
                    FROM movie_ratings \
                    GROUP BY movie_id) AS avg_ratings \
                JOIN movie_tags ON avg_ratings.movie_id = movie_tags.movie_id \
                WHERE rating_avg < 3.0 \
                GROUP BY tag \
                ORDER BY tag_count DESC'
    elif value =='high':
        query = 'SELECT tag, COUNT(*) AS tag_count \
                    FROM \
                    (SELECT \
                        movie_id, \
                        AVG(rating) AS rating_avg \
                        FROM movie_ratings \
                        GROUP BY movie_id) AS avg_ratings \
                    JOIN movie_tags ON avg_ratings.movie_id = movie_tags.movie_id \
                    WHERE rating_avg > 3.0 \
                    GROUP BY tag \
                    ORDER BY tag_count DESC'
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results

# returns a list of the number of tags that have been applied to each genre
def analyse_tag_genre_totals() -> List[Dict]:
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    query = 'SELECT genre, COUNT(*) AS tag_count \
                FROM movie_tags \
                JOIN movie_genre ON movie_tags.movie_id = movie_genre.movie_id \
                JOIN genres ON movie_genre.genre_id = genres.genre_id \
                GROUP BY genre'
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results

# returns a list of the number of tags that have been applied for each rating range 
def analyse_tag_rating_totals() -> List[Dict]:
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    query = 'SELECT \
                CASE \
                    WHEN rating_avg >= 0.5 AND rating_avg < 1 THEN \'0.5-1\' \
                    WHEN rating_avg >= 1 AND rating_avg < 1.5 THEN \'1-1.5\' \
                    WHEN rating_avg >= 1.5 AND rating_avg < 2 THEN \'1.5-2\' \
                    WHEN rating_avg >= 2 AND rating_avg < 2.5 THEN \'2-2.5\' \
                    WHEN rating_avg >= 2.5 AND rating_avg < 3 THEN \'2.5-3\' \
                    WHEN rating_avg >= 3 AND rating_avg < 3.5 THEN \'3-3.5\' \
                    WHEN rating_avg >= 3.5 AND rating_avg < 4 THEN \'3.5-4\' \
                    WHEN rating_avg >= 4 AND rating_avg < 4.5 THEN \'4-4.5\' \
                    ELSE \'4.5-5\' \
                END AS rating_range, \
                COUNT(*) as tag_count \
            FROM \
            (SELECT \
                movie_id, \
                AVG(rating) AS rating_avg \
                FROM movie_ratings \
                GROUP BY movie_id) AS avg_ratings \
            JOIN movie_tags ON avg_ratings.movie_id = movie_tags.movie_id \
            GROUP BY rating_range \
            ORDER BY rating_range ASC'
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results