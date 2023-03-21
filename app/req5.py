from typing import List, Dict
import datetime
import mysql.connector

config = {
        'user': 'team7',
        'password': 'G3LqY5UUTo0fK6x7nc7Q',
        'host': 'db',
        'port': '3306',
        'database': 'movie_db'
    }

def getQry(movieId) -> List[Dict]:
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    # query = "SELECT AVG(mr.rating) FROM movie_ratings AS mr WHERE mr.movie_id = 1 GROUP BY mr.movie_id"
    
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

    cursor.execute(query, (movieId,))
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results