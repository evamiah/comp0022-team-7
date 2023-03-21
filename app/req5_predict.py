from typing import List, Dict
import mysql.connector

config = {
        'user': 'team7',
        'password': 'G3LqY5UUTo0fK6x7nc7Q',
        'host': 'db',
        'port': '3306',
        'database': 'movie_db'
    }

# returns predicted aggregate rating for movie
def get_qry(movie_id) -> List[Dict]:
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    
    # takes around 20% of users in random that rated the movie into subset

    # finds the variance of users' ratings for previous movies and the previous movies' 
    # aggragate ratings to calculate the predicted rating for this movie_id

    query = "SELECT ROUND(AVG(mo.rating + \
        (SELECT AVG( \
        (SELECT AVG(mr.rating) \
        FROM movie_ratings AS mr \
        WHERE mr.movie_id = mu.movie_id \
        GROUP BY mr.movie_id) \
        - mu.rating) \
        FROM movie_ratings AS mu \
        WHERE mu.user_id = mo.user_id \
        GROUP BY mu.user_id)),1) AS predicted_rating \
        FROM movie_ratings AS mo \
        WHERE mo.movie_id = %s AND RAND() <= .2 \
        GROUP BY mo.movie_id"

    cursor.execute(query, (movie_id,))
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results