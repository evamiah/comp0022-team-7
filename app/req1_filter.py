from typing import List, Dict
import mysql.connector

config = {
        'user': 'team7',
        'password': 'G3LqY5UUTo0fK6x7nc7Q',
        'host': 'db',
        'port': '3306',
        'database': 'movie_db'
    }

# returns filtered movie results
def get_query(start_year, end_year, sort_by, order, genre_list, and_or_or, rating) -> List[Dict]:
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    
    query_part_one = 'SELECT m.movie_id, m.title, m.release_year, m.overview, m.poster_path, \
        GROUP_CONCAT(DISTINCT g.genre ORDER BY g.genre ASC) AS genre_list, \
        ROUND(AVG(mr.rating),1) AS ordered_rating \
        FROM movies AS m \
        INNER JOIN \
        movie_ratings AS mr \
        ON m.movie_id = mr.movie_id \
        INNER JOIN \
        movie_genre AS mg \
        ON m.movie_id = mg.movie_id \
        INNER JOIN \
        genres AS g \
        ON mg.genre_id = g.genre_id'
    
    query_part_two = ' GROUP BY m.movie_id'

    year_check = True
    if ((not start_year) and (not end_year)):
        year_check = False

    query = query_part_one

    if genre_list:
        query = where_and(query)
        genre_query = get_genre_list(genre_list, and_or_or)
        query = query + genre_query

    if year_check:
        query = where_and(query)
        if(start_year and end_year):
            query = query + " m.release_year BETWEEN %s AND %s"
            exec_param = (start_year, end_year)
        elif(start_year  and (not end_year)):
            query = query + " m.release_year >= %s"
            exec_param = (start_year,)
        elif((not start_year) and end_year):
            query = query + " m.release_year <= %s"
            exec_param = (end_year,)

    query = query + query_part_two

    if(rating != "all"):
        ordered_rate = get_rating_query(rating)
        query = query +  " HAVING ordered_rating" + ordered_rate

    if (sort_by != None):
        query = get_order_by(query,sort_by,order)

    if year_check:
        cursor.execute(query, exec_param)
    else:
        cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results

def where_and(query):
    if "WHERE" in query:
        query = query + " AND"
    else:
        query = query + " WHERE"
    return query

# returns genre selection section in query
def get_genre_list(genre_types, connector):
    if (connector == "Any"):
        string = " g.genre IN ("
        for genre_element in genre_types:
            string = string + "'" + genre_element + "',"
        string = string[:-1]
        string = string + ")"
    else:
        string = f" m.movie_id in {get_genre_subquery(genre_types)}"
    return string

def get_genre_subquery(genre_types):
    string = f"(SELECT sub_genre_list.movie_id From {get_sub_genre_list()} WHERE "
    for genre_element in genre_types:
        string = f"{string} sub_genre_list.genre_list LIKE '%{genre_element}%' AND"  
    string = string[:-4]
    string = string + ")"
    return string

def get_sub_genre_list():
    return "(SELECT m.movie_id, GROUP_CONCAT(DISTINCT g.genre ORDER BY g.genre ASC) AS genre_list \
        FROM movies AS m \
        INNER JOIN \
        movie_genre AS mg \
        ON m.movie_id = mg.movie_id \
        INNER JOIN \
        genres AS g \
        ON mg.genre_id = g.genre_id \
        GROUP BY m.movie_id) AS sub_genre_list"

# returns order by section in query
def get_order_by(query,sort_by,order):
    if (sort_by=="Title"):
        query = query + " ORDER BY m.title"
    elif (sort_by=="Release Year"):
        query = query + " ORDER BY m.release_year"
    elif (sort_by=="Genre"):
        query = query + " ORDER BY genre_list"
    elif(sort_by=="Rating"):
        query = query + " ORDER BY ordered_rating"
    elif(sort_by=="Popularity"):
        query = query + " ORDER BY COUNT(mr.user_id)"
    if (order == "desc"):
        query = query + " DESC"
    return query

# returns rating comparison section in query
def get_rating_query(rating):
    q = ""
    if (rating == "rating1"):
        q = " >= 1"
    if (rating == "rating2"):
        q = " >= 2"
    if (rating == "rating3"):
        q = " >= 3"
    if (rating == "rating4"):
        q = " >= 4"
    if (rating == "rating5"):
        q = " = 5"
    return q