from typing import List, Dict
import datetime
import mysql.connector

config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'movie_db'
    }

def getQuery(startYear, endYear, rating, title, genre, andOrOr, sortBy) -> List[Dict]:
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    queryPartOne = 'SELECT m.title, m.release_year, GROUP_CONCAT(DISTINCT g.genre ORDER BY g.genre ASC), ROUND(AVG(mr.rating),1) AS ordered_rating \
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
    
    queryPartTwo = ' GROUP BY m.title, m.release_year'

    if ((startYear != None) and (endYear != None)):
        if (int(startYear) > int(endYear)):
            new_startYear = endYear
            endYear = startYear
            startYear = new_startYear
        else:
            startYear = startYear
            endYear = endYear
        year_check = 1
    elif ((startYear == None) and (endYear != None)):
        startYear = 1900
        year_check = 1
    elif ((startYear != None) and (endYear == None)):
        today = datetime.date.today()
        endYear = today.year
        year_check = 1
    elif ((startYear == None) and (endYear == None)):
        year_check = 0

    if (rating == None):
        rating_check = 0
    else:
        rating_check = 1

    if ((title == None) and (genre == None)):
        title_genre_check = 0
    elif ((title == None) and (genre != None)):
        genre_types = ','.join(genre)
        title_genre_check = 1
    elif ((title != None) and (genre == None)):
        title_genre_check = 2
    elif ((title != None) and (genre != None)):
        genre_types = ','.join(genre)
        title_genre_check = 3

    query = queryPartOne

    if (((title_genre_check == 1) or (title_genre_check == 3)) and (andOrOr == "and") and (andList != "")):
        query = whereAnd(query)
        andList = getGenreList(genre_types, "and")
        query = query + " genre_list IN" + andList

    if (((title_genre_check == 1) or (title_genre_check == 3)) and (andOrOr == "or")):
        query = whereAnd(query)
        orList = getGenreList(genre_types, "or")
        query = query + orList

    if ((title_genre_check == 2) or (title_genre_check == 3)):
        query = whereAnd(query)
        query = query + " m.title LIKE '%" + title + "%'"

    if(rating_check == 1):
        query = whereAnd(query)
        query = query +  " ordered_rating = " + rating

    if(year_check == 1):
        query = whereAnd(query)
        query = query + " m.release_year BETWEEN " + startYear + " AND " + endYear

    query = query + queryPartTwo

    if (sortBy != None):
        query = getOrderBy(query,sortBy)

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

def getOrderBy(query,sortBy):
    if (sortBy=="title"):
        query = query + " ORDER BY m.title"
    elif (sortBy=="year"):
        query = query + " ORDER BY m.release_year"
    elif (sortBy=="genre"):
        query = query + " ORDER BY genre_list"
    elif(sortBy=="rating"):
        query = query + " ORDER BY ordered_rating"
    elif(sortBy=="popularity"):
        query = query + " ORDER BY COUNT(mr.user_id)"
    if (sortBy[-4:] == "desc"):
        query = query + " DESC"
    return query