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

def getQuery(startYear, endYear, sortBy, order, genre_list, rating) -> List[Dict]:
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    
    queryPartOne = 'SELECT m.movie_id, m.title, m.release_year, m.overview, m.poster_path, GROUP_CONCAT(DISTINCT g.genre ORDER BY g.genre ASC) AS genre_list, ROUND(AVG(mr.rating),1) AS ordered_rating \
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
    
    queryPartTwo = ' GROUP BY m.movie_id'

    if ((not startYear) and (not endYear)):
        year_check = 0
    elif (startYear  and (not endYear)):
        year_check = 2
    elif ((not startYear) and endYear):
        year_check = 3
    else:
        year_check = 1

    if (rating == "all"):
        rating_check = 0
    else:
        rating_check = 1

    if (genre_list == []):
        genre_check = 0
    else:
        genre_check = 1

    query = queryPartOne

    if (genre_check == 1):
        query = whereAnd(query)
        andList = getGenreList(genre_list, "and")
        query = query + " g.genre IN" + andList

    if(year_check == 1):
        query = whereAnd(query)
        query = query + " m.release_year BETWEEN " + startYear + " AND " + endYear
    elif(year_check == 2):
        query = whereAnd(query)
        query = query + " m.release_year >= " + startYear
    elif(year_check == 3):
        query = whereAnd(query)
        query = query + " m.release_year <= " + endYear

    query = query + queryPartTwo

    if(rating_check == 1):
        orderedRate = getRatingQuery(rating)
        query = query +  " HAVING ordered_rating" + orderedRate

    if (sortBy != None):
        query = getOrderBy(query,sortBy,order)

    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results

def whereAnd(query):
    if "WHERE" in query:
        query = query + " AND"
    else:
        query = query + " WHERE"
    return query

def getGenreList(genre_types, connector):
    string = " ("
    if (connector == "and"):
        for genre_elem in genre_types:
            string = string + "'" + genre_elem + "',"
        string = string[:-1]
    else:
        for genre_elem in genre_types:
            string = string + " genre_list IN '" + genre_elem + "' OR"  
        string = string[:-3]
    string = string + ")"
    return string

def getOrderBy(query,sortBy,order):
    if (sortBy=="Title"):
        query = query + " ORDER BY m.title"
    elif (sortBy=="Release Year"):
        query = query + " ORDER BY m.release_year"
    elif (sortBy=="Genre"):
        query = query + " ORDER BY genre_list"
    elif(sortBy=="Rating"):
        query = query + " ORDER BY ordered_rating"
    elif(sortBy=="Popularity"):
        query = query + " ORDER BY COUNT(mr.user_id)"
    if (order == "desc"):
        query = query + " DESC"
    return query

def getRatingQuery(rating):
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